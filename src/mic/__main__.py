import sys
from pathlib import Path

import click
import mic
import semver
from mic import _utils, file
from mic.component.executor import execute, execute_docker
from mic.component.initialization import create_directory, render_gitignore, render_run_sh, render_io_sh, render_output, detect_framework, \
    render_dockerfile
from mic.config_yaml import fill_config_file_yaml, get_numbers_inputs_parameters, get_inputs_parameters, \
    add_configuration_files, add_outputs, create_config_file_yaml, get_spec, write_step, write_spec, get_key_spec
from mic.constants import DATA_DIRECTORY_NAME, Framework, SRC_DIR, handle, DOCKER_DIR, STEP_KEY, TOTAL_STEPS, \
    DOCKER_KEY, REPO_KEY, VERSION_KEY
from mic.credentials import configure_credentials, print_list_credentials
from mic.publisher.docker import publish_docker
from mic.publisher.github import create_local_repo_and_commit, push
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


@cli.command(short_help="Show mic version")
def version(debug=False):
    click.echo(f"{Path(sys.argv[0]).name} v{mic.__version__}")


@cli.command(short_help="Configure credentials", help="Configure your credentials to access the Model Catalog API, "
                                                      "GitHub and Docker features")
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
              help='Your email', required=True, default="mint@isi.edu", show_default=True)
@click.option('--password', prompt="Password",
              required=True, hide_input=True, help="Your password")
@click.option('--name', prompt='Name', help='Your name', required=True)
@click.option('--git_username', prompt='GitHub Username', help='Your GitHub Username', required=True)
@click.option('--git_token', prompt='GitHub API token', help='Your GitHub API token', required=True, hide_input=False)
@click.option('--dockerhub_username', prompt='Docker Username', help='Your Docker Username')
def configure(server, username, password, git_username, git_token, name, dockerhub_username, profile="default"):
    try:
        email = username
        configure_credentials(server, username, password, git_username, git_token, name, email, dockerhub_username,
                              profile)
    except Exception as e:
        click.secho("Unable to create configuration file", fg="red")


@cli.command(short_help="List configuration profiles",
             help="List credential parameters for mic profiles. Lists all profile configurations if no profile given")
@click.option(
    "--profile",
    "-p",
    envvar="MINT_PROFILE",
    type=str,
    default=None,
    metavar="<profile-name>",
    help="specify a specific profile to list"
)
@click.option(
    "--short",
    "-s",
    is_flag=True,
    help="Only show a list of profiles, not their contents"
)
def list_credentials(profile=None, short=False):
    print_list_credentials(profile, short)


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
def encapsulate():
    """Command to encapsulate your Model Configuration"""


@encapsulate.command(short_help="Create directories and subdirectories")
@click.argument(
    "model_configuration_name",
    type=click.Path(exists=False, dir_okay=True, file_okay=False, resolve_path=True),
    required=True
)
def step1(model_configuration_name):
    """
    Create the directories and subdirectories.

    mic encapsulate step1 <model_configuration_name>

    The argument: `model_configuration_name` is the name of your model configuration
     """
    try:
        model_dir_path = create_directory(Path('.'), model_configuration_name)
    except Exception as e:
        click.secho("Error: {} could not be created".format(model_configuration_name), fg="red")
        exit(1)

    render_gitignore(model_dir_path)
    create_config_file_yaml(model_dir_path)
    create_local_repo_and_commit(model_dir_path)


@encapsulate.command(short_help="Pass the inputs and parameters for your Model Configuration")
@click.option(
    "-f",
    "--mic_config_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    default="config.yaml"
)
@click.option(
    "-p",
    "--parameters",
    type=int,
    required=True,
    default=0
)
def step2(mic_config_file, parameters):
    """
    Create MIC_CONFIG_FILE (config.yaml).

    - Before to run this command, you must copy the files or directories of the model into the data directory

    - Then, you must pass the number of parameters using the option (-p)

    mic encapsulate step2 -f <mic_config_file> -p <number_of_parameters>

    The argument: `MODEL_DIRECTORY` is the directory of your model configuration
    """
    inputs_dir = Path(mic_config_file).parent / DATA_DIRECTORY_NAME
    if not inputs_dir.exists():
        exit(1)
    fill_config_file_yaml(Path(mic_config_file), inputs_dir, parameters)


@encapsulate.command(short_help="Create MINT wrapper using the config.yaml")
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

    mic encapsulate step3 -f <mic_config_file>
    """
    if not Path(mic_config_file).exists():
        click.secho("Error: {} doesn't exists".format(mic_config_file), fg="red")
        exit(1)
    config_path = Path(mic_config_file)
    model_directory_path = config_path.parent
    inputs, parameters, outputs, configs = get_inputs_parameters(config_path)
    number_inputs, number_parameters, number_outputs = get_numbers_inputs_parameters(config_path)
    run_path = render_run_sh(model_directory_path, inputs, parameters, number_inputs, number_parameters)
    render_io_sh(model_directory_path, inputs, parameters, configs)
    render_output(model_directory_path)
    spec = get_spec(config_path)
    write_step(config_path, spec, 3)
    click.secho("The MINT Wrapper has created: {}".format(run_path))


@encapsulate.command(short_help="If the configuration has config files, select them")
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

    mic encapsulate step4 -f <mic_config_file> [configuration_files]...

    For example,
    mic encapsulate step4 -f config.yaml data/example_dir/file1.txt  data/file2.txt
    """
    config_path = Path(mic_config_file)
    if not config_path.exists():
        exit(1)
    add_configuration_files(config_path, configuration_files)
    model_directory_path = config_path.parent
    inputs, parameters, outputs, configs = get_inputs_parameters(config_path)
    number_inputs, number_parameters, number_outputs = get_numbers_inputs_parameters(config_path)
    render_run_sh(model_directory_path, inputs, parameters, number_inputs, number_parameters)
    render_io_sh(model_directory_path, inputs, parameters, configs)
    render_output(model_directory_path)
    spec = get_spec(config_path)
    write_step(config_path, spec, 4)


@encapsulate.command(short_help="Optional - Run your model with your computational environment.")
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

    mic encapsulate step5 -f <mic_config_file>
    """
    mic_config_path = Path(mic_config_file)
    if not mic_config_path.exists():
        exit(1)
    execute(mic_config_path)
    spec = get_spec(mic_config_path)
    write_step(mic_config_path, spec, 5)


@encapsulate.command(short_help="Prepare your Docker Image")
@click.option(
    "-f",
    "--mic_config_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    default="config.yaml"
)
def step6(mic_config_file):
    """
    Create the Docker Image

    mic encapsulate step6 -f <mic_config_file>
    """
    mic_config_path = Path(mic_config_file)
    model_dir = mic_config_path.parent
    src_dir_path = model_dir / SRC_DIR
    framework = detect_framework(src_dir_path)
    if framework is None:
        framework = click.prompt("Select the language",
                                 show_choices=True,
                                 type=click.Choice(Framework, case_sensitive=False),
                                 value_proc=handle
                                 )

    if framework == Framework.GENERIC:
        bin_dir = model_dir / DOCKER_DIR / "bin"
        bin_dir.mkdir(exist_ok=True)
    dockerfile = render_dockerfile(model_dir, framework)
    click.secho("The Dockerfile has been created: {}".format(dockerfile))
    spec = get_spec(mic_config_path)
    write_step(mic_config_path, spec, 6)


@encapsulate.command(short_help="Build and run the Docker Image")
@click.option(
    "-f",
    "--mic_config_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    default="config.yaml"
)
def step7(mic_config_file):
    """
    Build and run the Docker image

    mic encapsulate step7 -f <mic_config_file>
    """
    mic_config_path = Path(mic_config_file)
    execute_docker(Path(mic_config_file))
    write_spec(mic_config_path, STEP_KEY, 7)



@encapsulate.command(short_help="Select the outputs")
@click.argument(
    "outputs",
    type=click.Path(exists=True, dir_okay=True, file_okay=True, resolve_path=True),
    required=True,
    nargs=-1
)
@click.option(
    "-f",
    "--mic_config_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    default="config.yaml"
)
def step8(mic_config_file, outputs):
    """
    Select the outputs
    For example,

    mic encapsulate step8 -f <mic_config_file> [outputs]...
    """
    mic_config_path = Path(mic_config_file)
    add_outputs(Path(mic_config_file), outputs)
    write_spec(mic_config_path, STEP_KEY, 8)


@encapsulate.command(short_help="Publish your code")
@click.option(
    "-f",
    "--mic_config_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    default="config.yaml"
)
@click.option(
    "--profile",
    "-p",
    envvar="MINT_PROFILE",
    type=str,
    default="default",
    metavar="<profile-name>",
)
def step9(mic_config_file, profile):
    """
    Select the outputs
    For example,

    mic encapsulate step9 -f <mic_config_file> [outputs]...
    """
    mic_config_path = Path(mic_config_file)
    model_dir = mic_config_path.parent
    url, version = push(model_dir, profile)
    write_spec(mic_config_path, REPO_KEY, url)
    write_spec(mic_config_path, VERSION_KEY, version)
    write_spec(mic_config_path, STEP_KEY, 9)
    docker_image = publish_docker(mic_config_path, profile, version)
    write_spec(mic_config_path, DOCKER_KEY, docker_image)
    click.secho("Repository: {}".format(url))
    click.secho("Version: {}".format(version))
    click.secho("Docker Image: {}".format(docker_image))



@encapsulate.command(short_help="Show status")
@click.option(
    "-f",
    "--mic_config_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    default="config.yaml"
)
def status(mic_config_file):
    mic_config_path = Path(mic_config_file)
    spec = get_spec(mic_config_path)
    click.secho("Step {} of {}".format(spec[STEP_KEY], TOTAL_STEPS))


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
