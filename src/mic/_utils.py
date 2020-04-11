import configparser
import logging
import os
import uuid
from pathlib import Path

import click
import modelcatalog
import requests
from modelcatalog import ApiException

MODEL_ID_URI = "https://w3id.org/okn/i/mint/"
__DEFAULT_MINT_API_CREDENTIALS_FILE__ = "~/.mint/credentials"


def generate_new_uri():
    return "{}{}".format(MODEL_ID_URI, str(uuid.uuid4()))


def check_credentials():
    if not Path(__DEFAULT_MINT_API_CREDENTIALS_FILE__).expanduser().exists():
        create_credentials()


def create_credentials(profile="default"):
    api_username = click.prompt("Model Catalog API Username")
    api_password = click.prompt("Model Catalog API Password", hide_input=True)

    credentials_file = Path(
        os.getenv("MINT_API_CREDENTIALS_FILE", __DEFAULT_MINT_API_CREDENTIALS_FILE__)
    ).expanduser()
    os.makedirs(str(credentials_file.parent), exist_ok=True)

    credentials = configparser.ConfigParser()
    credentials.optionxform = str

    if credentials_file.exists():
        credentials.read(credentials_file)

    credentials[profile] = {
        "api_username": api_username,
        "api_password": api_password
    }

    with credentials_file.open("w") as fh:
        credentials_file.parent.chmod(0o700)
        credentials_file.chmod(0o600)
        credentials.write(fh)
        click.secho(f"Success", fg="green")


def get_api():
    check_credentials()
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
    return modelcatalog.ApiClient(configuration=configuration), username


def login(username, password):
    api_instance = modelcatalog.DefaultApi()
    configuration = modelcatalog.Configuration()
    try:
        api_response = api_instance.user_login_get(username, password)
        access_token = api_response["access_token"]
        configuration.access_token = access_token

    except ApiException as e:
        logging.error("Exception when calling DefaultApi->user_login_get: %s\n" % e)
        quit()
    return configuration


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
