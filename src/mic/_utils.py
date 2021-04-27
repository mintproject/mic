import logging
import os
import platform
import re
from pathlib import Path

import click
import requests
import validators
from requests.auth import HTTPBasicAuth

import mic
from mic.constants import CONFIG_YAML_NAME, DIRECTORIES_TO_IGNORE, LOG_FILE, MIC_DIR

MODEL_ID_URI = "https://w3id.org/okn/i/mint/"
__DEFAULT_MINT_API_CREDENTIALS_FILE__ = "~/.mint/credentials"


def obtain_id(url):
    if validators.url(url):
        return url.split('/')[-1]


def first_line_new(resource, i=""):
    click.echo("======= {} ======".format(resource))
    click.echo("The actual values are:")



def get_filepaths(directory):
    """
    This function will generate the file names in a directory
    tree by walking the tree either top-down or bottom-up. For each
    directory in the tree rooted at directory top (including top itself),
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.

def make_log_file():
    if os.path.exists(Path(MIC_DIR) / LOG_FILE):
        return True
    try:
        if not os.path.exists(Path(MIC_DIR)):
            os.mkdir(MIC_DIR)
        if not os.path.exists(Path(MIC_DIR) / LOG_FILE):
            with open(Path(MIC_DIR) / LOG_FILE, 'w') as fp:
                pass

        init_logger()
        return True
    except Exception as e:
        click.secho("WARNING: Could not make log file: \"{}\"".format(e),fg="yellow")
        return False

def log_system_info(logger):
    log = logging.getLogger(logger)
    log.info("Log file created")
    try:
        plat_obj = {'name': platform.system(), 'data': {'version': platform.version(),
                                                       'release': platform.release(),
                                                       'platform': platform.platform()}}
    except Exception as e:
        log.warning("os obj got attribute error while making os object")
        try:
            plat_obj = {'name': os.name}
        except Exception as e:
            plat_obj = {'name': "Unknown os"}

    log.info("OS: {}".format(plat_obj))
    log.info("MIC Version: {}".format(mic.__version__))

def log_variable(logger, var, name="variable"):
    """
    Given a logger log a debug variable, logs variable's content and type. Optional: enter name field to give a
    descriptive name
    :param logger:
    :param var:
    :param name:
    :return:
    """
    logger.debug("{}: {}".format(name,{'content': var, 'type': type(var).__name__}))

def log_command(logger, command_name, **kwargs):
    """
    List the current command, enter option variables of command as kwargs to display what the inputs are.
    Ex: log_command(logging, "start", name="name", image="image")
    :param logger:
    :param command_name:
    :param kwargs:
    :return:
    """
    logger.info("<=================>")
    if len(kwargs) > 0:
        inp = {}
        for key, value in kwargs.items():
            inp[key] = {'value': value, 'type': type(value).__name__}

        logger.info("Command: {}".format({'name': command_name, 'command_parameters': inp }))
    else:
        logger.info("Command: {}".format(command_name))

def get_mic_logger():
    return logging.getLogger(mic.__name__)


def init_logger():
    logger = logging.getLogger(mic.__name__)
    if os.path.exists(Path(MIC_DIR) / LOG_FILE):
        handler = logging.FileHandler(Path(MIC_DIR) / LOG_FILE)
    elif os.path.exists(LOG_FILE):
        handler = logging.FileHandler(LOG_FILE)
    else:
        handler = logging.StreamHandler()
    formatter = logging.Formatter("%(name)-5s %(filename)-18s %(levelname)-8s %(message)s")
    handler.setFormatter(formatter)

    #Remove all other handlers before adding new one
    for i in logger.handlers:
        logger.removeHandler(i)

    logger.addHandler(handler)
    logger.setLevel(logging.WARNING)

def get_latest_version():
    try:
        return requests.get("https://pypi.org/pypi/mic/json").json()["info"]["version"]
    except Exception as e:
        raise e


def check_mic_path(mic_dir):
    if mic_dir is None:
        mic_file = recursive_mic_search(os.getcwd())
        if mic_file is None:
            click.secho("Could not find {}. Please specify a path with -f".format(CONFIG_YAML_NAME),fg="red")
            exit(1)
        else:
            click.echo("Found {} in {}".format(CONFIG_YAML_NAME, mic_file))
            return mic_file
    else:
        return mic_dir


def recursive_mic_search(curr_dir):
    """
    Recursively search for mic.yaml (CONFIG_YAML_NAME) down from the current dir. Return path if fount else return None
    :param curr_dir:
    :return abs_path_to_mic:
    """
    # Check for files first
    for file in os.listdir(curr_dir):
        file = os.path.join(curr_dir, file)
        if not os.path.isdir(file):
            # Return if it finds mic.yaml
            if file.split(os.sep)[-1] == CONFIG_YAML_NAME:
                return os.path.abspath(os.path.join(curr_dir, file))

    # Recurse down dirs
    for file in os.listdir(curr_dir):
        file = os.path.join(curr_dir, file)
        if os.path.isdir(file) and file not in DIRECTORIES_TO_IGNORE:
            next = recursive_mic_search(os.path.abspath(file))
            if next is not None:
                return next

    # Default case
    return None

def find_dir(name, path):
    for root, dirs, files in os.walk(path):
        if os.path.basename(root) == name:
            return root

def parse(value):
    try:
        return int(value)
    except:
        return value


def upload_code(upload_file: Path):
    """Upload a file using HTTP and HTTP basic

    Args:
        upload_file (Path): Path to the file

    Raises:
        SystemExit: Exit the cli if there a error

    Returns:
        [Response]: [description]
    """
    server = "https://publisher.mint.isi.edu"
    url = f"""{server}/{upload_file.name}"""
    user = "upload"
    password = "HVmyqAPWDNuk5SmkLOK2"
    header = {'Content-Type': 'application/binary'}
    try:
        with open(upload_file, 'rb') as f:
            r = requests.put(url, headers=header, data=f, verify=True, auth=HTTPBasicAuth(user, password))
        r.raise_for_status()
        return r
    except requests.exceptions.Timeout as e:
        # Maybe set up for a retry, or continue in a retry loop
        logging.error(e)
        exit(1)
    except requests.exceptions.TooManyRedirects as e:
        # Tell the user their URL was bad and try a different one
        logging.error(e)
        exit(1)
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        raise SystemExit(e)


def download(url: str):
    """Download file using HTTP
    Args:
        url (str): Path to the file

    Raises:
        SystemExit: Exit the cli if there a error

    Returns:
        [Response]: [description]
    """
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r
    except requests.exceptions.Timeout as e:
        # Maybe set up for a retry, or continue in a retry loop
        logging.error(e)
        exit(1)
    except requests.exceptions.TooManyRedirects as e:
        # Tell the user their URL was bad and try a different one
        logging.error(e)
        exit(1)
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        raise SystemExit(e)
