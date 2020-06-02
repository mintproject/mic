import logging
import os
import re
import uuid
import click
import requests
import validators
from mic._mappings import Metadata_types

MODEL_ID_URI = "https://w3id.org/okn/i/mint/"
__DEFAULT_MINT_API_CREDENTIALS_FILE__ = "~/.mint/credentials"


def path_walk(top, topdown = False, followlinks = False):
    """
         See Python docs for os.walk, exact same behavior but it yields Path() instances instead
    """
    names = list(top.iterdir())

    dirs = (node for node in names if node.is_dir() is True)
    nondirs =(node for node in names if node.is_dir() is False)

    if topdown:
        yield top, dirs, nondirs

    for name in dirs:
        if followlinks or name.is_symlink() is False:
            for x in path_walk(name, topdown, followlinks):
                yield x

    if topdown is not True:
        yield top, dirs, nondirs


def generate_new_uri():
    return "{}{}".format(MODEL_ID_URI, str(uuid.uuid4()))


def obtain_id(url):
    if validators.url(url):
        return url.split('/')[-1]

def first_line_new(resource, i=""):
    click.echo("======= {} ======".format(resource))
    click.echo("The actual values are:")


def init_logger():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG if os.getenv("CAPS_CLI_DEBUG", False) else logging.INFO)


def get_latest_version():
    return requests.get("https://pypi.org/pypi/mic/json").json()["info"]["version"]


def validate_metadata(default_type, value):
    if default_type == Metadata_types.Url:
        regex = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        return re.match(regex, value)
    elif default_type == Metadata_types.Float:
        try:
            convert_to_float = float(value)
            return True
        except ValueError as ve:
            return False
