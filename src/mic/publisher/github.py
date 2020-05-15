from pathlib import Path
from github import Github
from mic.credentials import get_credentials
import click
import logging
import os
import zipfile
import base64


def publish_github(directory: Path, profile):
    """
    Publish the directory on git
    If the directory is not a git directory, create it
    If the git directory doesn't have a remote origin, create a github repository
    @param profile:
    @param directory:
    @type directory:
    """
    git_username = None
    git_token = None

    try:
        credentials = get_credentials(profile)
        git_username = credentials["gitUsername"]
        git_token = credentials["gitToken"]
    except KeyError:
        click.secho("WARNING: The profile is malformed, To configure it, run:\nmic configure -p {}".format(profile),
                    fg="yellow")
        exit(1)

    g = Github(git_username, git_token)
    path = str(Path.cwd())
    repo_name = os.path.split(path)[1]
    repo = None

    # Get the repo for the given model directory. Make new repo if it does not exist
    if is_git_directory(g, repo_name):
        repo = g.get_user().get_repo(repo_name)
    else:
        logging.info("Repo does not exist. Generating new repo")
        repo = git_init(g, repo_name)

    # TODO Check if file already exists before uploading file
    zip_path = compress_src_dir(path, repo_name)

    print(zip_path)
    data = open(zip_path, "rb").read()

    repo.create_file(path=repo_name + ".zip", message="Created " + repo_name, content=data)

    try:
        os.remove(zip_path)
    except Exception as e:
        logging.error("Could not remove zip file")
        click.secho(e, fg="red")
        exit(1)

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


def compress_src_dir(directory, name):
    """
    Compress the directory src and create a zip file
    @param directory: Path
    @param name: string
    @return path: Path
    """

    file_paths = []

    # walks through given directory and appends path to a list of paths that should be zipped
    for root, directories, files in os.walk(directory):
        for filename in files:
            # join the two strings in order to form the full filepath.
            filepath = os.path.relpath(os.path.join(root, filename), directory)
            file_name = os.path.split(filepath)[1]

            # Adds path if it is within src
            if "src" in filepath:
                file_paths.append(filepath)

            # Adds path if file is a json or dockerfile
            if ".json" in file_name or ".dockerfile" in file_name:
                file_paths.append(filepath)

    if os.path.exists(os.path.join(directory, (name + ".zip"))):
        logging.error("\"" + name + ".zip" + "\" already exists in model. "
                                             "Please remove it before publishing, or use force option")
        exit(1)

    with zipfile.ZipFile(os.path.join(directory, (name + ".zip")), 'w') as zipper:
        # writing each file one by one
        for file in file_paths:
            zipper.write(file)

    return os.path.join(directory, (name + ".zip"))


def git_push():
    pass


def git_release():
    """
    Use https://pygithub.readthedocs.io/en/latest/github_objects/GitRelease.html#github.GitRelease.GitRelease.update_release

    If there is a release, increment the version.
    """
    pass
