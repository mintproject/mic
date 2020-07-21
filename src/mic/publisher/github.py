import datetime
import logging
import os
import re
import shutil
from pathlib import Path

import click
import pygit2 as pygit2
import semver
from distutils.version import StrictVersion
from github import Github
from mic.config_yaml import write_spec
from mic.constants import MINT_COMPONENT_ZIP, GIT_TOKEN_KEY, GIT_USERNAME_KEY, SRC_DIR, REPO_KEY, VERSION_KEY, \
    MINT_COMPONENT_KEY, DEFAULT_CONFIGURATION_WARNING
from mic.credentials import get_credentials

author = pygit2.Signature('MIC Bot', 'bot@mint.isi.edu')


def push(model_directory: Path, mic_config_path: Path, name: str, profile):
    repository_name = name
    click.secho("Creating the git repository")
    repo = get_local_repo(model_directory)
    click.secho("Compressing your code")
    compress_src_dir(model_directory)
    click.secho("Creating a new commit")
    git_commit(repo)
    click.secho("Creating or using the GitHub repository")
    url = check_create_remote_repo(repo, profile, repository_name)
    repository_name = url.split('/')[-1].replace(".git", "")
    write_spec(mic_config_path, REPO_KEY, url)
    click.secho("Creating a new version")
    _version = git_tag(repo, author)

    click.secho("Pushing your changes to the server")
    remote = repo.remotes["origin"]
    try:
        git_pull(repo, remote)
    except AssertionError as e:
        click.secho("Unable to handle git conflict, please fix them manually", fg="red")
        exit(1)

    git_push(repo, profile, _version)
    write_spec(mic_config_path, VERSION_KEY, _version)

    repo = get_github_repo(profile, repository_name)
    file = None
    for i in repo.get_contents(""):
        if i.name == "{}.zip".format(MINT_COMPONENT_ZIP):
            file = i
            write_spec(mic_config_path, MINT_COMPONENT_KEY, file.download_url)
            break
    if not file:
        click.secho(f"Mint component not found {MINT_COMPONENT_ZIP}.zip", fg="red")
        exit(1)
    click.secho("Repository: {}".format(url))
    click.secho("Version: {}".format(_version))


def git_commit(repo):
    repo.index.add_all()
    repo.index.write()
    tree = repo.index.write_tree()
    parent = None
    try:
        parent = repo.revparse_single('HEAD')
    except KeyError:
        pass

    parents = []
    if parent:
        parents.append(parent.oid.hex)
    repo.create_commit('refs/heads/master', author, author, "automated mic", tree, parents)


def get_local_repo(model_path: Path):
    if pygit2.discover_repository(model_path):
        return pygit2.Repository(pygit2.discover_repository(model_path))
    else:
        return pygit2.init_repository(model_path, False)


def compress_src_dir(model_path: Path):
    """
    Compress the directory src and create a zip file
    """
    zip_file_name = model_path / MINT_COMPONENT_ZIP
    src_dir = model_path / SRC_DIR
    mic_component_path = model_path / f"{MINT_COMPONENT_ZIP}.zip"
    if mic_component_path.exists():
        os.remove(mic_component_path)
    zip_file_path = shutil.make_archive(zip_file_name.name, 'zip', root_dir=model_path.parent,
                                        base_dir=src_dir.relative_to(model_path.parent))
    shutil.move(zip_file_path, mic_component_path)
    return zip_file_path


def check_create_remote_repo(repo, profile, model_name):
    if "origin" in [i.name for i in repo.remotes]:
        origin__url = repo.remotes["origin"].url

        try:
            github_repo_exists(model_name, profile)
        except Exception:
            click.secho(f"The git repository has a remote server configured {origin__url}, "
                        f"but it does not exist on github", fg="red")
            click.echo("You can delete the reference to the repository running\n$ git remote remove origin")
            exit(1)

        click.secho(f"The git repository has a remote server configured {origin__url}")
        return origin__url
    else:
        click.secho(f"The git repository has not a remote server configured ")
        click.secho(f"Creating a new repository on GitHub")
        repo_github = github_create_repo(profile, model_name)
        url = repo_github.clone_url
        repo.remotes.create("origin", url)
        git_push(repo, profile)
        click.secho(f"The url is: {url}")
        return url


def get_github_repo(profile, model_name):
    git_token, git_username = github_config(profile)
    g = Github(git_username, git_token)
    github_login(g)
    user = g.get_user()
    return user.get_repo(model_name)


def git_add_remote(repo, url):
    repo.remotes.create("origin", url)


def git_pull(repo, remote, branch="master"):
    remote.fetch()
    remote_master_id = repo.lookup_reference('refs/remotes/origin/%s' % (branch)).target
    merge_result, _ = repo.merge_analysis(remote_master_id)
    # Up to date, do nothing
    if merge_result & pygit2.GIT_MERGE_ANALYSIS_UP_TO_DATE:
        return True
    elif merge_result & pygit2.GIT_MERGE_ANALYSIS_FASTFORWARD:
        repo.checkout_tree(repo.get(remote_master_id))
        try:
            master_ref = repo.lookup_reference('refs/heads/%s' % (branch))
            master_ref.set_target(remote_master_id)
        except KeyError:
            repo.create_branch(branch, repo.get(remote_master_id))
        repo.head.set_target(remote_master_id)
    elif merge_result & pygit2.GIT_MERGE_ANALYSIS_NORMAL:
        repo.merge(remote_master_id)

        if repo.index.conflicts is not None:
            for conflict in repo.index.conflicts:
                click.echo(f"Conflicts found in: {conflict[0].path}")
            raise AssertionError('Conflicts')

        user = repo.default_signature
        tree = repo.index.write_tree()
        commit = repo.create_commit('HEAD',
                                    user,
                                    user,
                                    'Merge',
                                    tree,
                                    [repo.head.target, remote_master_id])
        # We need to do this or git CLI will think we are still merging.
        repo.state_cleanup()
    else:
        raise AssertionError('Unknown merge analysis result')


def git_push(repo, profile, tag=None):
    git_token, git_username = github_config(profile)
    callbacks = pygit2.RemoteCallbacks(pygit2.UserPass(git_token, 'x-oauth-basic'))
    remote = repo.remotes["origin"]
    remote.push(['refs/heads/master'], callbacks=callbacks)
    if tag:
        remote.push(['refs/tags/{}'.format(tag)], callbacks=callbacks)


def git_tag(repo, tagger):
    """
    If there is a release, increment the version.
    """
    version = get_next_tag(repo)
    repo.create_tag(str(version),
                    repo.revparse_single('HEAD').oid.hex,
                    pygit2.GIT_OBJ_COMMIT,
                    tagger,
                    str(version))

    click.secho("New version: {}".format(str(version)))
    return str(version)


def get_next_tag(repo):
    regex = re.compile('^refs/tags')
    _tags = filter(lambda r: regex.match(r), repo.listall_references())
    tags = [tag.split('/')[-1] for tag in _tags]
    tags.sort(key=StrictVersion)
    today = datetime.date.today()
    version_today = semver.VersionInfo.parse("{}.{}.{}".format(int(today.year) % 100, today.month, 1))
    if tags:
        version_str = tags[-1]
        try:
            version = semver.VersionInfo.parse(version_str)
            click.secho("Previous version {}".format(version))
            if int(version.minor) != today.month or int(version.major) != today.year % 100:
                return version_today
            else:
                return version.bump_patch()
        except ValueError as e:
            logging.info(e)
            pass
    return version_today


def github_create_repo(profile, model_name):
    """
    Upload the directory to git
    If the directory is not a git directory, create it
    If the git directory doesn't have a remote origin, create a github repository
    @type profile: str
    @param profile: the profile to use in the credentials file
    @type: directory: Path
    """
    g = github_auth(profile)
    user = g.get_user()

    repo = None
    try:
        repo = user.get_repo(model_name)
    except:
        # TODO: github.GithubException.UnknownObjectException: 404
        # {"message": "Not Found", "documentation_url": "https://developer.github.com/v3/repos/#get"}
        pass
    if repo:
        if not click.confirm("The repo {} exists. Do you want to use it?".format(model_name), default=True):
            click.secho("Please rename the directory", fg="green")
            exit(0)
    else:
        repo = user.create_repo(model_name)
    return repo


def github_repo_exists(model_name, profile):
    g = github_auth(profile)
    try:
        g.get_user().get_repo(model_name)
    except Exception as e:
        raise e


def github_auth(profile):
    git_token, git_username = github_config(profile)
    g = Github(git_username, git_token)
    github_login(g)
    return g


def remove_temp_files(model_path: Path):
    component_folder = model_path / "{}_component".format(model_path.name)
    zip_folder = model_path / "{}.zip".format(MINT_COMPONENT_ZIP)
    try:
        if component_folder.exists():
            shutil.rmtree(component_folder)

        if zip_folder.exists():
            os.remove(zip_folder)

    except:
        click.secho("Warning: error when removing temporary files", fg="yellow")


def github_config(profile):
    # Try to get git username and token from credentials file
    try:
        credentials = get_credentials(profile)
        git_username = credentials[GIT_USERNAME_KEY]
        git_token = credentials[GIT_TOKEN_KEY]
    except KeyError:
        click.secho(DEFAULT_CONFIGURATION_WARNING + " {}".format(profile), fg="yellow")
        exit(1)
    return git_token, git_username


def github_login(g, debug=False):
    try:
        if g.get_user().login is None:
            logging.error("User profile GitHub credentials are invalid. Please enter a valid token and username")
            exit(1)
    # I know its bad to except Exception but it doesnt catch it when I except TypeError, and the only way this *should*
    # fail is if the credentials are bad so...
    except Exception as e:
        logging.error("User profile GitHub credentials are invalid. Please enter a valid token and username")
        if debug:
            click.secho(e, fg="yellow")
        exit(1)
