from pathlib import Path
from github import Github
from mic.credentials import get_credentials
import click
import logging


def publish_github(directory: Path, profile):
    """
    Publish the directory on git
    If the directory is not a git directory, create it
    If the git directory doesn't have a remote origin, create a github repository
    @param profile:
    @param directory:
    @type directory:
    """
    try:
        credentials = get_credentials(profile)
        gitUsername = credentials["gitUsername"]
        gitToken = credentials["gitToken"]
    except KeyError:
        click.secho("WARNING: The profile is malformed, To configure it, run:\nmic configure -p {}".format(profile),
                    fg="yellow")
        exit(1)

    g = Github(gitUsername, gitToken)
    # TODO dont hardcode the name
    repo_name = "wcm2"
    repo = None

    # Get the repo for the given model directory. Make new repo if it does not exist
    if is_git_directory(g, repo_name):
        repo = g.get_user().get_repo(repo_name)
    else:
        logging.info("Repo does not exist. Generating new repo")
        repo = git_init(g, repo_name)

    # TODO upload directory to the repo
    print(repo.name)
    # try:
    #     if not is_git_directory():
    #         git_init()
    #     if not is_has_remote_branch():
    #         create_github_repository()
    #     compress_src_dir()
    #     git_add()
    #     git_commit()
    #     git_release()
    #     git_push()
    #
    # except Exception as e:
    #     raise e


def create_github_repository():
    pass


def is_has_remote_branch():
    return True


def git_commit():
    pass


def is_git_directory(gitObj, name):
    """
    Returns True if user already owns a repository with the model's name.
    False otherwise
    @param gitObj: github
    @param name: string
    """
    repo_list = gitObj.get_user().get_repos(type="owner")

    for i in repo_list:
        if name == i.name:
            return True

    return False


def git_init(gitObj, name):
    """
    Creates a new repository with the given name under the users repositories
    @param gitObj: github
    @param name: string
    @return repo: github.repository
    """
    user = gitObj.get_user()
    return user.create_repo(name)


def git_add():
    pass


def compress_src_dir():
    """
    Compress the directory src and create a zip file
    """
    pass


def git_push():
    pass


def git_release():
    """
    Use https://pygithub.readthedocs.io/en/latest/github_objects/GitRelease.html#github.GitRelease.GitRelease.update_release

    If there is a release, increment the version.
    """
    pass
