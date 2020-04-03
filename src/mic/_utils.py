import ast
import configparser
import json
import logging
import os
import uuid
from pathlib import Path

import click
import modelcatalog
import requests
from modelcatalog import ApiException

MODEL_ID_URI = "https://w3id.org/okn/i/mint/"


def generate_new_uri():
    return "{}{}".format(MODEL_ID_URI, str(uuid.uuid4()))


def get_api_configuration():
    __DEFAULT_MINT_API_CREDENTIALS_FILE__ = "~/.mint_api/credentials"
    credentials_file = Path(
        os.getenv("MINT_API_CREDENTIALS_FILE", __DEFAULT_MINT_API_CREDENTIALS_FILE__)
    ).expanduser()
    credentials = configparser.ConfigParser()
    credentials.optionxform = str
    if credentials_file.exists():
        credentials.read(credentials_file)
    profile = "default"
    username = credentials[profile]["api_username"]
    password = credentials[profile]["api_password"]
    configuration = login(username, password)
    return configuration, username


def login(username, password):
    api_instance = modelcatalog.DefaultApi()
    configuration = modelcatalog.Configuration()
    try:
        api_response = api_instance.user_login_get(username, password)
        data = json.dumps(ast.literal_eval(api_response))
        access_token = json.loads(data)["access_token"]
        configuration.access_token = access_token

    except ApiException as e:
        logging.error("Exception when calling DefaultApi->user_login_get: %s\n" % e)
        quit()
    return configuration

def first_line_new(resource, i=""):
    click.echo("======= {} ======".format(resource))


def ask_simple_value(variable_name, resource_name, default_value=None):
    value = click.prompt('{} - {} '.format(resource_name, variable_name), default=default_value)
    return [value]


def init_logger():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG if os.getenv("CAPS_CLI_DEBUG", False) else logging.INFO)


def get_latest_version():
    return requests.get("https://pypi.org/pypi/mic/json").json()["info"]["version"]
