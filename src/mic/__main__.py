import configparser
import logging
import os
import sys
from pathlib import Path
import json

import click

import semver

import mic
from mic import _utils, _metadata_schema, _transform_data, _initialize, _push, _validate
from mic._modelconfiguration import create as modelconfiguration_create
from mic._model import create as create_model


__DEFAULT_CAPS_CLI_CREDENTIALS_FILE__ = "~/.mic/credentials"
__DEFAULT_MINT_API_CREDENTIALS_FILE__ = "~/.mint_api/credentials"


@click.group()
@click.option("--verbose", "-v", default=0, count=True)
def cli(verbose):
    _utils.init_logger()
    lv = ".".join(_utils.get_latest_version().split(".")[:3])
    cv = ".".join(mic.__version__.split(".")[:3])

    if semver.compare(lv, cv) > 0:
        click.secho(
            f"""WARNING: You are using mic version {mic.__version__}, however version {lv} is available.
You should consider upgrading via the 'pip install --upgrade mic' command.""",
            fg="yellow",
        )


@cli.command(short_help="Show mic version.")
def version(debug=False):
    click.echo(f"{Path(sys.argv[0]).name} v{mic.__version__}")


@cli.command(help="Configure Model Catalog API credentials")
@click.option(
    "--profile",
    "-p",
    envvar="CAPS_PROFILE",
    type=str,
    default="default",
    metavar="<profile-name>",
)
def configure(profile="default"):
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

@cli.group()
def modelconfiguration():
    """Manages setups"""

@modelconfiguration.command(short_help="Add a modelconfiguration")
@click.option(
    "--inputs",
    "-i",
    type=int,
    default=0,
)
@click.option(
    "--outputs",
    "-o",
    type=int,
    default=0,
)
@click.option(
    "--parameters",
    "-p",
    type=int,
    default=0,
)
def add(inputs=0, outputs=0, parameters=0, directory=""):
    modelconfiguration_create(inputs, outputs, parameters)
    click.secho(f"Success", fg="green")

@cli.group()
def model():
    """Manages setups"""

@model.command(short_help="Add a model")
def add(inputs=0, outputs=0, parameters=0, directory=""):
    create_model()
    click.secho(f"Success", fg="green")




