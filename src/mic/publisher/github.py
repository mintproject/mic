from pathlib import Path


def publish_github(directory: Path):
    """
    Publish the directory on git
    If the directory is not a git directory, create it
    If the git directory doesn't have a remote origin, create a github repository
    @param directory:
    @type directory:
    """
    try:
        if not is_git_directory():
            git_init()
        if not is_has_remote_branch():
            create_github_repository()
        compress_src_dir()
        git_add()
        git_commit()
        git_release()
        git_push()

    except Exception as e:
        raise e


def create_github_repository():
    pass


def is_has_remote_branch():
    return True


def git_commit():
    pass


def is_git_directory():
    return True


def git_init():
    pass


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
