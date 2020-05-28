import datetime
import logging
import re
import shutil
from pathlib import Path

import click
import pygit2 as pygit2
import semver
from mic.config_yaml import write_spec
from distutils.version import StrictVersion
from github import Github
from mic.constants import MINT_COMPONENT_ZIP, GIT_TOKEN_KEY, GIT_USERNAME_KEY, SRC_DIR, REPO_KEY, VERSION_KEY, \
    MINT_COMPONENT_KEY
from mic.credentials import get_credentials

author = pygit2.Signature('MIC Bot', 'bot@mint.isi.edu')


def create_local_repo_and_commit(model_directory: Path):
    """
    Publish the directory on git
    If the directory is not a git directory, create it
    If the git directory doesn't have a remote origin, create a github repository
    @param directory:
    @type directory:
    """
    try:
        repo = get_or_create_repo(model_directory)
        git_commit(repo)
    except Exception as e:
        raise e


def push(model_directory: Path, mic_config_path: Path, profile):
    click.secho("Creating the git repository")
    repo = get_or_create_repo(model_directory)
    click.secho("Compressing your code")
    compress_src_dir(model_directory)
    click.secho("Creating a new commit")
    git_commit(repo)
    click.secho("Creating or using the GitHub repository")
    url = check_create_remote_repo(repo, profile, model_directory.name)
    click.secho("Creating a new version")
    _version = git_tag(repo, author)
    click.secho("Pushing your changes to the server")
    git_push(repo, profile, _version)
    repo = get_github_repo(profile, model_directory.name)
    for i in repo.get_contents(""):
        if i.name == "{}.zip".format(MINT_COMPONENT_ZIP):
            file = i
            break

    write_spec(mic_config_path, REPO_KEY, url)
    write_spec(mic_config_path, VERSION_KEY, _version)
    write_spec(mic_config_path, MINT_COMPONENT_KEY, file.download_url)
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


def get_or_create_repo(model_path: Path):
    return pygit2.Repository(pygit2.discover_repository(model_path)) if pygit2.discover_repository(
        model_path) else pygit2.init_repository(
        model_path, False)


def compress_src_dir(model_path: Path):
    """
    Compress the directory src and create a zip file
    """
    zip_file_name = model_path / MINT_COMPONENT_ZIP
    tmp_dir = model_path / "{}_component".format(model_path.name)
    shutil.copytree(model_path / SRC_DIR, tmp_dir / SRC_DIR)
    zip_file_path = shutil.make_archive(zip_file_name.name, 'zip', root_dir=model_path, base_dir=tmp_dir.name)
    return zip_file_path

def check_create_remote_repo(repo, profile, model_name):
    if "origin" in repo.remotes:
        try:
            return repo.remotes["origin"].url
        except:
            pass
    try:
        return repo.remotes["origin"].url
    except:
        repo = github_create_repo(profile, model_name)
        url = repo.clone_url
        repo.remotes.create("origin", url)
        return url


def get_github_repo(profile, model_name):
    git_token, git_username = github_config(profile)
    g = Github(git_username, git_token)
    github_login(g)
    user = g.get_user()
    return user.get_repo(model_name)


def git_add_remote(repo, url):
    repo.remotes.create("origin", url)


def git_push(repo, profile, tag):
    git_token, git_username = github_config(profile)
    callbacks = pygit2.RemoteCallbacks(pygit2.UserPass(git_token, 'x-oauth-basic'))
    remote = repo.remotes["origin"]
    remote.push(['refs/heads/master'], callbacks=callbacks)
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
    Publish the directory on git
    If the directory is not a git directory, create it
    If the git directory doesn't have a remote origin, create a github repository
    @type profile: str
    @param profile: the profile to use in the credentials file
    @type: directory: Path
    """

    git_token, git_username = github_config(profile)
    g = Github(git_username, git_token)
    github_login(g)
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
            click.echo("Please rename the directory")
            exit(0)
    else:
        repo = user.create_repo(model_name)
    return repo


def github_config(profile):
    # Try to get git username and token from credentials file
    try:
        credentials = get_credentials(profile)
        git_username = credentials[GIT_USERNAME_KEY]
        git_token = credentials[GIT_TOKEN_KEY]
    except KeyError:
        click.secho("WARNING: Could not find GitHub credentials in profile, "
                    "please run:\nmic configure -p {}".format(profile), fg="yellow")
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
