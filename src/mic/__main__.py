import sys
from pathlib import Path

import click
import mic
import semver
from mic import _utils, file
from mic.component.executor import execute
from mic.component.initialization import create_directory, render_run_sh, render_io_sh, render_output, detect_framework, \
    render_dockerfile
from mic.config_yaml import create_file_yaml, get_numbers_inputs_parameters, get_inputs_parameters, \
    add_configuration_files
from mic.constants import DATA_DIRECTORY_NAME, Framework, SRC_DIR, handle
from mic.credentials import configure_credentials
from mic.publisher.docker import publish_docker
from mic.publisher.github import publish_github
from mic.publisher.model_catalog import publish_model_catalog
from mic.resources.model import create as create_model
from modelcatalog import Configuration, DatasetSpecification, Parameter


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
@click.argument(
    "model_configuration_name",
    type=click.Path(exists=False, dir_okay=True, file_okay=False, resolve_path=True),
    required=True
)
def step1(model_configuration_name):
    """
    Create the directories and subdirectories.

    mic modelconfiguration step1 <model_configuration_name>

    The argument: `model_configuration_name` is the name of your model configuration
     """
    try:
        create_directory(Path('.'), model_configuration_name)
    except Exception as e:
        exit(1)


@modelconfiguration.command(short_help="Create directories and subdirectories")
@click.option(
    "-i",
    "--inputs_dir",
    type=click.Path(exists=False, dir_okay=True, file_okay=False, resolve_path=True),
    required=False,
)
@click.option(
    "-p",
    "--parameters",
    type=int,
    required=True,
    default=0
)
@click.argument(
    "model_directory",
    type=click.Path(exists=False, dir_okay=True, file_okay=False, resolve_path=True),
    required=True
)
def step2(model_directory, inputs_dir, parameters):
    """
    Create MIC_CONFIG_FILE (config.yaml).

    - Before to run this command, you must copy the files or directories of the model into the data directory

    - Then, you must pass the number of parameters using the option (-p)

    mic modelconfiguration step2 <model_directory> -p <number_of_parameters>

    The argument: `MODEL_DIRECTORY` is the directory of your model configuration
    """
    inputs_dir = Path(inputs_dir) if inputs_dir else Path(model_directory) / DATA_DIRECTORY_NAME
    create_file_yaml(Path(model_directory), inputs_dir, parameters)


@modelconfiguration.command(short_help="Create MINT wrapper using the config.yaml")
@click.option(
    "-f",
    "--mic_config_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    default="config.yaml"
)
def step3(mic_config_file):
    """
    Create MINT wrapper using the config.yaml

    - You must pass the MIC_CONFIG_FILE (config.yaml) using the option (-f).

    mic modelconfiguration step3 -f config.yaml
    """
    if not Path(mic_config_file).exists():
        click.secho("Error: {} doesn't exists".format(mic_config_file), fg="red")
        exit(1)
    config_path = Path(mic_config_file)
    model_directory_path = config_path.parent
    inputs, parameters, outputs = get_inputs_parameters(config_path)
    number_inputs, number_parameters, number_outputs = get_numbers_inputs_parameters(config_path)
    render_run_sh(model_directory_path, inputs, parameters, number_inputs, number_parameters)
    render_io_sh(model_directory_path)
    render_output(model_directory_path)


@modelconfiguration.command(short_help="Create MINT wrapper using the config.yaml")
@click.argument(
    "configuration_files",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    required=True,
    nargs=-1
)
@click.option(
    "-f",
    "--mic_config_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    default="config.yaml"
)
def step4(mic_config_file, configuration_files):
    """
    THIS IS STEP IS OPTIONAL

    Select the inputs files that are configuration files

    - You must pass the MIC_CONFIG_FILE (config.yaml) using the option (-f).

    - And the files as arguments

    mic modelconfiguration step4 -f config.yaml [configuration_files]...

    For example,
    mic modelconfiguration step4 -f config.yaml data/example_dir/file1.txt  data/file2.txt
    """
    if not Path(mic_config_file).exists():
        exit(1)
    add_configuration_files(Path(mic_config_file), configuration_files)


@modelconfiguration.command(short_help="Create MINT wrapper using the config.yaml")
@click.option(
    "-f",
    "--mic_config_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    default="config.yaml"
)
def step5(mic_config_file):
    """
    Running your model in your computer with your computational environment.
    For example,

    mic modelconfiguration step5 -f config.yaml
    """
    if not Path(mic_config_file).exists():
        exit(1)
    execute(Path(mic_config_file))


@modelconfiguration.command(short_help="Building Docker Image using the config.yaml")
@click.option(
    "-f",
    "--mic_config_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    default="config.yaml"
)
def step6(mic_config_file):
    """
    Create the Docker Image
    For example,

    mic modelconfiguration step6 -f config.yaml
    """
    model_dir = Path(mic_config_file).parent
    src_dir_path = model_dir / SRC_DIR
    if detect_framework(src_dir_path) is None:
        language = click.prompt("Select the language",
                              show_choices=True,
                              type=click.Choice(Framework, case_sensitive=False),
                              value_proc=handle
                              )
        render_dockerfile(model_dir, language)

    pass


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
