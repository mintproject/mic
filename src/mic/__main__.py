import sys
from pathlib import Path

import click
import mic
import semver
from mic.credentials import configure_credentials
from mic import _utils, file
from mic._model import create as create_model
from mic._modelconfiguration import create as modelconfiguration_create

__DEFAULT_MINT_API_CREDENTIALS_FILE__ = "~/.mint_api/credentials"

from modelcatalog import Configuration


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
@click.option(
    "--profile",
    "-p",
    envvar="MINT_PROFILE",
    type=str,
    default="default",
    metavar="<profile-name>",
)
@click.option('--server', prompt='Model Catalog API',
              help='The Model Catalog API', required=True, default=Configuration().host, show_default=True)
@click.option('--username', prompt='Username',
              help='Your email.', required=True, default="mint@isi.edu", show_default=True)
@click.option('--password', prompt="Password",
              required=True, hide_input=True, help="Your password")
def configure(server, username, password, profile="default"):
    configure_credentials(server, username, password, profile)


@cli.group()
def model():
    """Command to create and edit Models"""


@model.command(short_help="Add a model")
def add(inputs=0, outputs=0, parameters=0, directory=""):
    create_model()
    click.secho(f"Success", fg="green")


@model.command(short_help="Load a model from file")
@click.option(
    "--filename",
    "-f",
    required=True,
    prompt="Please type the path to the file",
    type=click.Path(exists=True, file_okay=True, resolve_path=True),
)
def load(filename):
    request = file.load(filename)
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
