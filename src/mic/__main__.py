import sys
from pathlib import Path

import click
import semver
from modelcatalog import Configuration, ModelConfiguration, DatasetSpecification, Parameter

import mic
from mic import _utils, file
from mic.component.initialization import create_directory, render_run_sh, render_io_sh, render_dockerfile
from mic.credentials import configure_credentials
from mic.file import save
from mic.resources.model import create as create_model
from mic.resources.model_configuration import create as model_configuration_create


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


@modelconfiguration.command(short_help="Create a modelconfiguration")
@click.option(
    "--profile",
    "-p",
    envvar="MINT_PROFILE",
    type=str,
    default="default",
    metavar="<profile-name>",
)
def add(profile):
    from mic.resources.software_version import SoftwareVersionCli
    model_configuration_create(profile=profile, parent=SoftwareVersionCli)
    click.secho(f"Success", fg="green")


@cli.group()
def component():
    """Command to handle components"""


@component.command(short_help="Init a component")
@click.option(
    "--name",
    "-n",
    type=str,
    prompt=True,
    required=True
)
@click.option(
    "--inputs",
    "-i",
    type=int,
    default=0
)
@click.option(
    "--outputs",
    "-o",
    type=int,
    default=0
)
@click.option(
    "--parameters",
    "-p",
    type=int,
    default=0
)
@click.option(
    "-d",
    "--directory",
    type=click.Path(exists=False, dir_okay=True, file_okay=False, resolve_path=True),
    default="."
)
@click.option(
    "-l",
    "--language",
    default="generic"
)
def init(name, inputs, outputs, parameters, directory, language):
    model_configuration = ModelConfiguration()
    _inputs = []
    _outputs = []
    _parameters = []
    for i in range(0, inputs):
        _inputs.append(DatasetSpecification(label="Input {}".format(i+1), position=i+1))
    for i in range(0, inputs):
        _outputs.append(DatasetSpecification(label="Output {}".format(i+1), position=i+1))
    for i in range(0, inputs):
        _parameters.append(Parameter(label="Parameter {}".format(i+1), position=i+1))

    if _inputs:
        model_configuration.has_input = _inputs
    if _outputs:
        model_configuration.has_output = _outputs
    if _parameters:
        model_configuration.has_parameter = _parameters
    model_configuration.label = name

    component_dir = create_directory(Path(directory), name)
    render_run_sh(component_dir, inputs, parameters, outputs, language)
    render_io_sh(component_dir)
    render_dockerfile(component_dir, language)

    save(model_configuration.to_dict(), file_name=component_dir / ".{}.json".format(name))

