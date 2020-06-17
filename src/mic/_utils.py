import logging
import os
import re

import click
import requests
import validators
from mic._mappings import Metadata_types

MODEL_ID_URI = "https://w3id.org/okn/i/mint/"
__DEFAULT_MINT_API_CREDENTIALS_FILE__ = "~/.mint/credentials"


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
    try:
        return requests.get("https://pypi.org/pypi/mic/json").json()["info"]["version"]
    except Exception as e:
        raise e


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


def find_dir(name, path):
    for root, dirs, files in os.walk(path):
        if os.path.basename(root) == name:
            return root
