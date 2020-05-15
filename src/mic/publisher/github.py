from pathlib import Path
from github import Github
from mic.credentials import get_credentials
import click
import logging
import os
import zipfile


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
    debug = False

    try:
        credentials = get_credentials(profile)
        git_username = credentials["gitUsername"]
        git_token = credentials["gitToken"]
    except KeyError:
        click.secho("WARNING: Could not find GitHub credentials in profile, "
                    "please run:\nmic configure -p {}".format(profile), fg="yellow")
        exit(1)

    g = Github(git_username, git_token)

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

    if debug:
        logging.info("User has " + str(g.rate_limiting[0]) + " API calls left of " + str(g.rate_limiting[1]) + " total")

    path = str(Path.cwd())
    repo_name = os.path.split(path)[1]
    repo = None
    content_does_not_exist = False
    content = None

    # Get the repo for the given model directory. Make new repo if it does not exist
    if is_git_directory(g, repo_name):
        repo = g.get_user().get_repo(repo_name)
    else:
        logging.info("Repo does not exist. Generating new repo")
        repo = git_init(Path, g, repo_name)
        content_does_not_exist = True

    # TODO, what happens if README in local and remote are different? (Error if different but allow if force is used)
    # TODO Let github credentials be added from within cli
    # TODO robust debug mode. Git api requests. Make everything try, throw exception if debug on

    zip_path = compress_src_dir(path, repo_name)

    data = open(zip_path, "rb").read()

    # Check if file is already in repo
    if not content_does_not_exist:  # if statement just skips extra api call if mic made new repo
        found = False
        content = repo.get_contents(path="")
        for stuff in content:
            if stuff.name == repo_name + ".zip":
                found = True
                content = stuff

        if not found:
            content_does_not_exist = True

    if content_does_not_exist:
        logging.info("Creating " + repo_name + ".zip")
        repo.create_file(path=repo_name + ".zip", message="Created " + repo_name, content=data)
    else:
        if content.decoded_content != data:
            logging.info("Updating " + repo_name + ".zip")
            repo.update_file(path=repo_name + ".zip", message="Updated " + repo_name, content=data, sha=content.sha)
        else:
            logging.info("This version of model already exists in GitHub repository. No change made")

    try:
        os.remove(zip_path)
    except Exception as e:
        logging.warning("Could not remove zip file")
        click.secho(e, fg="yellow")


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


def has_remote_branch():
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


def git_init(path, gitObj, name):
    """
    Creates a new repository with the given name under the users repositories
    Checks if README exists in current path. Creates new README if one does not already exist
    @param path: path
    @param gitObj: github
    @param name: string
    @return repo: github.repository
    """
    user = gitObj.get_user()
    repo = user.create_repo(name)

    path = os.path.join(path.cwd(), "README.md")

    if os.path.exists(path):
        logging.info("Uploading README to repo")
        data = open("README.md", "r").read()
        repo.create_file(path="README.md", message="Uploaded README", content=data)

    else:
        # Make README
        try:
            logging.info("No README found. Creating new one")
            readme = open("README.md", "w+")
            readme.write("Documentation for " + name + " goes here")
            readme.close()

            data = open("README.md", "r").read()
            repo.create_file(path="README.md", message="Created README", content=data)
            os.remove("README.md")

        except Exception as e:
            logging.warning("Error while trying to create README file")
            click.secho("Error message: " + str(e), fg="yellow")

    return repo


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
