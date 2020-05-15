import sys
from pathlib import Path

import click
import semver
from modelcatalog import Configuration, DatasetSpecification, Parameter

import mic
from mic import _utils, file
from mic.component.initialization import create_directory
from mic.config_yaml import create_file_yaml, DATA_DIRECTORY_NAME
from mic.credentials import configure_credentials
from mic.publisher.docker import publish_docker
from mic.publisher.github import publish_github
from mic.publisher.model_catalog import publish_model_catalog
from mic.resources.model import create as create_model


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
    try:
        configure_credentials(server, username, password, profile)
    except Exception as e:
        click.secho("Unable to create configuration file", fg="red")


@cli.group()
def model():
    """Command to create and edit Models"""


@model.command(short_help="Add a model")
@click.option(
    "--profile",
    "-p",
    envvar="MINT_PROFILE",
    type=str,
    default="default",
    metavar="<profile-name>",
)
def add(profile):
    create_model(profile=profile)
    click.secho(f"Success", fg="green")


@model.command(short_help="Load a model from file")
@click.option(
    "--filename",
    "-f",
    required=True,
    prompt="Please type the path to the file",
    type=click.Path(exists=True, file_okay=True, resolve_path=True),
)
@click.option(
    "--profile",
    "-p",
    envvar="MINT_PROFILE",
    type=str,
    default="default",
    metavar="<profile-name>",
)
def load(filename, profile):
    request = file.load(filename)
    create_model(profile=profile, request=request)
    click.secho(f"Success", fg="green")


@cli.group()
def modelconfiguration():
    """Command to create and edit ModelConfigurations"""


@modelconfiguration.command(short_help="Publish")
@click.option(
    "-d",
    "--directory",
    type=click.Path(exists=False, dir_okay=True, file_okay=False, resolve_path=True),
    default="."
)
def publish(directory):
    try:
        publish_docker()
        publish_github()
        publish_model_catalog()
    except Exception as e:
        exit(1)


@modelconfiguration.command(short_help="Create directories and subdirectories")
@click.option(
    "-n",
    "--name",
    type=str,
    required=True,
    prompt=True
)
def skeleton(name):
    try:
        create_directory(Path('.'), name)
    except Exception as e:
        exit(1)


@modelconfiguration.command(short_help="Create directories and subdirectories")
@click.option(
    "-p",
    "--parameters",
    type=int,
    required=True,
    default=0
)
@click.argument(
    "directory",
    type=click.Path(exists=False, dir_okay=True, file_okay=False, resolve_path=True),
    required=True
)
def init(directory, parameters):
    create_file_yaml(Path(directory), Path(directory) / DATA_DIRECTORY_NAME, parameters)


def prepare_inputs_outputs_parameters(inputs, model_configuration, name):
    _inputs = []
    _outputs = []
    _parameters = []
    for i in range(0, inputs):
        _inputs.append(DatasetSpecification(label="Input {}".format(i + 1), position=i + 1))
    for i in range(0, inputs):
        _outputs.append(DatasetSpecification(label="Output {}".format(i + 1), position=i + 1))
    for i in range(0, inputs):
        _parameters.append(Parameter(label="Parameter {}".format(i + 1), position=i + 1))
    if _inputs:
        model_configuration.has_input = _inputs
    if _outputs:
        model_configuration.has_output = _outputs
    if _parameters:
        model_configuration.has_parameter = _parameters
    model_configuration.label = name
