from pathlib import Path
from github import Github
from mic.credentials import get_credentials
import click
import logging
import os
import zipfile


def publish_github(directory: Path, profile, force, tag, message):
    """
    Publish the directory on git
    If the directory is not a git directory, create it
    If the git directory doesn't have a remote origin, create a github repository

    @type profile: str
    @param profile: the prodile to use in the credentials file

    @type: directory: Path
    @param directory: path to the model's directory

    @type force: bool
    @param force: should publish be forced to run, ignoring override protection

    @type tag: str
    @param tag: name for the release tag

    @type message: str
    @param message: message for release
    """

    git_username = None
    git_token = None
    debug = False

    # Try to get git username and token from credentials file
    try:
        credentials = get_credentials(profile)
        git_username = credentials["gitUsername"]
        git_token = credentials["gitToken"]
    except KeyError:
        click.secho("WARNING: Could not find GitHub credentials in profile, "
                    "please run:\nmic configure -p {}".format(profile), fg="yellow")
        exit(1)

    # Create github object
    g = Github(git_username, git_token)

    # Check if the credentials from the file are valid
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
        logging.debug("User has " + str(g.rate_limiting[0]) + " API calls left of " + str(g.rate_limiting[1]) + " total")

    path = str(directory)
    # remove trailing path separators
    path = path.rstrip("\\")
    path = path.rstrip("/")
    os.chdir(path)  # forgive this sin. Setting current dir to path makes this so much easier

    repo_name = os.path.split(path)[1]
    zip_name = repo_name + ".zip"
    repo = None
    content_does_not_exist = False
    content = None

    # Get the repo for the given model directory. Make new repo if it does not exist
    if is_git_directory(g, repo_name):
        repo = g.get_user().get_repo(repo_name)
    else:
        logging.info("Repo does not exist. Generating new repo")
        repo = git_init(directory, g, repo_name)
        content_does_not_exist = True

    # TODO robust debug mode. Git api requests remaining. Make everything try, throw exception if debug on
    # TODO documentation

    # Zip the files in the
    zip_path = compress_src_dir(path, repo_name, force)
    data = open(zip_path, "rb").read()

    # Check if file is already in repo
    if not content_does_not_exist:  # this if statement just skips extra api call if mic already created a new repo
        found = False
        content = repo.get_contents(path="")
        for stuff in content:
            if stuff.name == zip_name:
                found = True
                content = stuff

        if not found:
            content_does_not_exist = True

    # Create or update file (depending on if one already exists)
    if content_does_not_exist:
        logging.info("Zipping files")
        repo.create_file(path=zip_name, message="Created " + repo_name, content=data)

        # Generate new release
        logging.info("Generating new release")
        update_release(repo, tag, message)
    else:
        # Check if there is a discrepancy between local README (if it exists) and GitHub README
        if os.path.exists(os.path.join(path, "README.md")):
            local_readme = open("README.md", "rb").read()

            # If force flag is used the remote README will be updated to the local one
            try:
                if repo.get_readme().decoded_content != local_readme:
                    if force:
                        repo.update_file(path="README.md", message="Updated README", content=local_readme, sha=repo.get_readme().sha)
                        logging.info("Updating remote README from local")
                    else:
                        logging.warning("Local README does not match remote README")
                        logging.info("Either delete local README to keep remote version or "
                                     "use \"--force\" flag to override remote readme")
                        exit(1)
            except Exception as e:
                # If there is no README in the repo make new one from current
                repo.create_file(path="README.md", message="Created README", content=local_readme)

        # Checks if content has changed then updates remote files with local ones and create release
        if content.decoded_content != data or force:
            if force and content.decoded_content == data:
                logging.info("Forcing publish")
            else:
                logging.info("Updating " + zip_name)
            repo.update_file(path=zip_name, message="Updated " + repo_name, content=data, sha=content.sha)

            # increment release
            logging.info("Incrementing release")
            update_release(repo, tag, message)
        else:
            logging.info("This version of model already exists in GitHub repository."
                         " \"-f\" can be used to force release")

    # Tries to delete the zip file generated while zipping
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


def is_git_directory(gitObj, name):
    """
    Returns True if user already owns a repository with the model's name. False otherwise

    @type gitObj: github
    @param gitObj: Object for the github class

    @type name: repository name to check
    @param name: string

    @rtype bool
    @return: Whether there is a git directory with this name already
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

    @type path: Path
    @param path: Path of model

    @type gitObj: github
    @param gitObj: github object with token credentials

    @type name: str
    @param name: name of repository

    @rtype: repo: github.repository
    @return repo: object for the repository to modify
    """

    user = gitObj.get_user()
    repo = user.create_repo(name)  # Create new repository

    readme_path = os.path.join(path, "README.md")

    # if README already exists
    if os.path.exists(readme_path):
        logging.info("Uploading README to repo")
        data = open("README.md", "r").read()
        repo.create_file(path="README.md", message="Uploaded README", content=data)

    else:
        # Create a README in the repository
        try:
            logging.info("No README found. Creating new one")
            readme = open("README.md", "w+")
            readme.write("Documentation for " + name + " goes here")  # Auto generated content for README
            readme.close()

            data = open("README.md", "r").read()
            repo.create_file(path="README.md", message="Created README", content=data)
            os.remove("README.md")

        except Exception as e:
            logging.warning("Error while trying to create README file")
            click.secho("Error message: " + str(e), fg="yellow")

    return repo


def compress_src_dir(directory, name, force):
    """
    Compress the directory src and create a zip file

    @type directory: Path
    @param directory:

    @type name: str
    @param name: name for the zipped file

    @type force: bool
    @param force: flag to override file if zip file with same name already exists

    @rtype path: Path
    @return path: Path to the zipped file
    """

    file_paths = []

    # Remove any trailing os separators (Very likely user input issue)
    directory = directory.rstrip("\\")
    directory = directory.rstrip("/")

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
        if force:
            try:
                logging.info("Removing existing zip file")
                os.remove(os.path.join(directory, (name + ".zip")))
            except PermissionError as e:
                logging.error("mic does not have permissions to remove \"" +
                              os.path.join(directory, (name + ".zip")) + "\"")
                logging.info("Please remove the file and retry")
                exit(1)
        else:
            logging.error("\"" + name + ".zip" + "\" already exists in model. "
                                                 "Please remove it before publishing, or use force option")
            exit(1)

    with zipfile.ZipFile(os.path.join(directory, (name + ".zip")), 'w') as zipper:
        # writing each file one by one
        for file in file_paths:
            zipper.write(file)

    return os.path.join(directory, (name + ".zip"))


def update_release(repo, tag_name, message):
    """
    If there is a release already, increment it by new version. If tag_name is entered create the new release with
    entered tag_name. Create new release if one does not exist

    @type repo: github.Repository
    @param repo: repository object for the model

    @type tag_name: str
    @param tag_name: GitHub tag for the commit

    @type message: str
    @param message: GitHub message for the release

    @rtype release: github.GitRelease
    @return release: release object
    """

    releases = repo.get_releases()

    # If no tag_name is given auto generate tag_name from number of previous releases
    if tag_name is None:
        tag_name = str(releases.totalCount + 1) + ".0.0"

    # Make sure the tag name does not exist in the repo
    tag_already_taken = False
    for r in releases:
        if r.tag_name == tag_name:
            tag_already_taken = True

    # If no message given, provide auto generated message
    if message is None:
        message = "Release " + tag_name + " for " + repo.name

    if tag_already_taken:
        logging.warning("There is already a release with that version tag in the repository")
        logging.info("Use --tag option to give model a different version tag and rerun")
        return None
    else:
        repo.create_git_release(tag_name, tag_name, message)
        return repo.get_latest_release()

