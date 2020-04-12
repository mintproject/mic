import sys
from pathlib import Path

import click

import semver

import mic
from mic._utils import create_credentials
from mic import _utils, file
from mic._modelconfiguration import create as modelconfiguration_create
from mic._model import create as create_model

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


@cli.command(help="Configure your credentials to access the Model Catalog API ")
def configure():
    create_credentials()

@cli.group()
def model():
    """Command to create and edit Models"""


@model.command(short_help="Add a model")
def add(inputs=0, outputs=0, parameters=0, directory=""):
    create_model()
    click.secho(f"Success", fg="green")


@model.command(short_help="Load a model from file")
def load(inputs=0, outputs=0, parameters=0, directory=""):
    request = file.load()
    create_model(request)
    click.secho(f"Success", fg="green")


@cli.group()
def modelconfiguration():
    """Command to create and edit ModelConfigurations"""


@modelconfiguration.command(short_help="Create a modelconfiguration")
def add():
    from mic._software_version import SoftwareVersionCli
    modelconfiguration_create(parent=SoftwareVersionCli)
    click.secho(f"Success", fg="green")
