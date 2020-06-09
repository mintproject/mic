import sys
from pathlib import Path

import mic
import semver
from dame.utils import obtain_id
from mic import _utils, file
from mic.cli_docs import *
from mic.component.executor import execute_using_docker
from mic.component.initialization import create_directory, render_run_sh, render_io_sh, render_output, \
    render_dockerfile, render_gitignore, detect_framework
from mic.component.python3 import freeze
from mic.config_yaml import fill_config_file_yaml, get_numbers_inputs_parameters, get_inputs_parameters, \
    add_configuration_files, create_config_file_yaml, get_spec, write_spec, get_key_spec
from mic.constants import *
from mic.credentials import configure_credentials, print_list_credentials
from mic.publisher.docker import publish_docker
from mic.publisher.github import create_local_repo_and_commit, push
from mic.publisher.model_catalog import create_model_catalog_resource, publish_model_configuration
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
def credentials(server, username, password, git_username, git_token, name, dockerhub_username, profile="default"):
    try:
        email = username
        configure_credentials(server, username, password, git_username, git_token, name, email, dockerhub_username,
                              profile)
    except Exception as e:
        click.secho("Unable to create configuration file", fg="red")


@cli.command(short_help="List credentials profiles",
             help="List credential parameters for mic profiles. Lists all profile credentials if no profile given")
@click.option(
    "--profile",
    "-p",
    envvar="MINT_PROFILE",
    type=str,
    default=None,
    metavar="<profile-name>",
    help="specify a profile to list"
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


@encapsulate.command(short_help="Set up a MIC directory structure and MIC file template")
@click.argument(
    "model_configuration_name",
    type=click.Path(exists=False, dir_okay=True, file_okay=False, resolve_path=True),
    required=True
)
def step1(model_configuration_name):
    """
    Generates mic.yaml and the directories (data/, src/, docker/) for your model component. Also initializes a local
    GitHub repository

    The argument: `model_configuration_name` is the name of your model configuration

    Example:
    mic encapsulate step1 <model_configuration_name>
    """
    new_directory = Path(".") / model_configuration_name
    if new_directory.exists():
        click.secho("The directory {} already exists, please use another name".format(new_directory.name), fg="red")
        exit(1)
    try:
        model_dir_path = create_directory(Path('.'), model_configuration_name)
    except Exception as e:
        click.secho("Error: {} could not be created".format(model_configuration_name), fg="red")
        exit(1)

    render_gitignore(model_dir_path)
    create_config_file_yaml(model_dir_path)
    create_local_repo_and_commit(model_dir_path)
    click.secho("MIC has initialized the component. {}/, {}/, {}/ and {} created".format(DATA_DIR, DOCKER_DIR, SRC_DIR,
                                                                                         CONFIG_YAML_NAME))
    click.secho(
        "Before step2 you must add your data (files or directories) into the {} directory: {}".format(
            DATA_DIR, model_dir_path / DATA_DIR),
        fg='green')


@encapsulate.command(short_help="Pass the inputs and parameters for your Model Configuration")
@click.option(
    "-p",
    "--parameters",
    type=int,
    required=True,
    default=0
)
@click.option(
    "-f",
    "--mic_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    default=CONFIG_YAML_NAME
)
def step2(mic_file, parameters):
    """
    Fill the MIC configuration file with the information about the parameters and inputs

    MIC is going to detect:
     - the inputs (files and directory) and add them in the MIC configuration file.
     - the parameters and add them in the configuration file

    Example:
    mic encapsulate step2 -f <mic_file> -p <number_of_parameters>
    """
    mic_config_path = Path(mic_file)
    inputs_dir = mic_config_path.parent / DATA_DIRECTORY_NAME
    if not inputs_dir.exists():
        exit(1)
    fill_config_file_yaml(Path(mic_file), inputs_dir, parameters)
    click.secho("MIC has added the parameters and inputs into the {} ({})".format(MIC_CONFIG_FILE_NAME,
                                                                                  CONFIG_YAML_NAME))
    click.secho("You can see the changes in {}".format(Path(mic_file).absolute()), fg="green")
    click.secho("Before step3: ", fg="green")
    click.secho("You must add a default value for the \"default-value\" field in {}. Just replace the 0 with your value"
                "".format(CONFIG_YAML_NAME),
                fg="green")
    click.secho("It is recommended you also add a description for each input and parameter in {}".format(CONFIG_YAML_NAME),
                fg="green")
    click.secho("If you use a script to initialize or create visualizations of your model you must copy these into the "
                "src directory", fg="green")
    write_spec(mic_config_path, STEP_KEY, 2)

    
@encapsulate.command(short_help="Create MINT wrapper using the " + CONFIG_YAML_NAME)
@click.option(
    "-f",
    "--mic_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    default=CONFIG_YAML_NAME
)
def step3(mic_file):
    """
    Create MINT wrapper using the mic.yaml. This command will handle adding inputs and parameters into the run file.

    - You must pass the MIC_FILE (mic.yaml) using the option (-f) or run the command from the same directory as mic.yaml

    Example:
    mic encapsulate step3 -f <mic_file>
    """
    if not Path(mic_file).exists():
        click.secho("Error: {} doesn't exists".format(mic_file), fg="red")
        exit(1)
    mic_config_path = Path(mic_file)
    model_directory_path = mic_config_path.parent
    inputs, parameters, outputs, configs = get_inputs_parameters(mic_config_path)
    number_inputs, number_parameters, number_outputs = get_numbers_inputs_parameters(mic_config_path)
    run_path = render_run_sh(model_directory_path, inputs, parameters, number_inputs, number_parameters)
    render_io_sh(model_directory_path, inputs, parameters, configs)
    render_output(model_directory_path, [], False)
    write_spec(mic_config_path, STEP_KEY, 3)
    click.echo("The MIC Wrapper has been created at: {}".format(run_path))
    click.secho("Before the next step you must add any (bash) commands needed to run your model between the two "
                "comments in the wrapper file. This file is located in {}/{}".format(SRC_DIR, RUN_FILE), fg="green")
    click.secho("If your model has a configuration file, you will need to edit the values to match {}\'s parameter "
                "names then run step4. Otherwise you can move on to step5. See the docs for more details"
                "".format(CONFIG_YAML_NAME), fg="green")


@encapsulate.command(short_help="Select configuration file(s) for your model. If there are any")
@click.argument(
    "configuration_files",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    required=True,
    nargs=-1
)
@click.option(
    "-f",
    "--mic_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    default=CONFIG_YAML_NAME
)
def step4(mic_file, configuration_files):
    """
    If your model does not use configuration files, you can skip this step

    Specify the inputs and parameters of your model component from configuration file(s)

    - You must pass the MIC_FILE (mic.yaml) using the option (-f) or run the command from the same directory as mic.yaml

    - Pass the configuration files as arguments

    mic encapsulate step4 -f <mic_file> [configuration_files]...

    Example:
    mic encapsulate step4 -f mic.yaml data/example_dir/file1.txt  data/file2.txt
    """
    mic_config_path = Path(mic_file)
    if not mic_config_path.exists():
        click.secho("Error: that configuration path does not exist", fg="red")
        exit(1)

    # loop through configuration_files list
    for cp in configuration_files:
        # The program will crash if the users configuration file is not in the data dir. This checks for that
        if DATA_DIR not in Path(cp).absolute().parts:
            click.secho("Error: Configuration file must be stored within {} directory".format(DATA_DIR), fg="red")
            click.secho("Bad path input: {}".format(cp))
            exit(1)
    add_configuration_files(mic_config_path, configuration_files)
    model_directory_path = mic_config_path.parent
    inputs, parameters, outputs, configs = get_inputs_parameters(mic_config_path)
    number_inputs, number_parameters, number_outputs = get_numbers_inputs_parameters(mic_config_path)
    render_run_sh(model_directory_path, inputs, parameters, number_inputs, number_parameters)
    render_io_sh(model_directory_path, inputs, parameters, configs)
    render_output(model_directory_path, [], False)
    write_spec(mic_config_path, STEP_KEY, 4)


@encapsulate.command(short_help="Create Docker image")
@click.option(
    "-f",
    "--mic_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    default=CONFIG_YAML_NAME
)
def step5(mic_file):
    """
    Set up Docker Image for model.

    Example:
    mic encapsulate step5 -f <mic_file>
    """
    mic_config_path = Path(mic_file)
    model_dir = mic_config_path.parent
    src_dir_path = model_dir / SRC_DIR
    if not mic_config_path.exists():
        exit(1)
    frameworks = detect_framework(src_dir_path)
    if len(frameworks) > 1:
        click.secho("MIC has detect {} possible framework/language on component: {}".format(
            len(frameworks), ",".join([i.label for i in frameworks])))

        click.secho("Please select the correct option")
        click.secho("This information allows MIC to select the correct Docker Image")
        framework = click.prompt("Select a option ".format(Framework),
                                 show_choices=True,
                                 type=click.Choice(frameworks, case_sensitive=False),
                                 value_proc=handle
                                 )
    elif len(frameworks) == 1:
        framework = frameworks[0]
    else:
        framework = Framework.GENERIC

    if framework == Framework.GENERIC:
        bin_dir = model_dir / DOCKER_DIR / "bin"
        bin_dir.mkdir(exist_ok=True)
    elif framework == Framework.PYTHON37:
        requirements_file = Path(mic_file).parent / DOCKER_DIR / REQUIREMENTS_FILE
        freeze(requirements_file)
        click.echo("Extracting the Python dependencies.\nYou can view or edit the dependencies file {} ".format(
            requirements_file))
    dockerfile = render_dockerfile(model_dir, framework)
    click.secho("Dockerfile has been created: {}".format(dockerfile))
    write_spec(mic_config_path, STEP_KEY, 5)


@encapsulate.command(short_help="Build and run the Docker Image")
@click.option(
    "-f",
    "--mic_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    default=CONFIG_YAML_NAME
)
def step6(mic_file):
    """
    Build and run the Docker image

    Example:
    mic encapsulate step6 -f <mic_file>
    """
    mic_config_path = Path(mic_file)
    execute_using_docker(Path(mic_file))
    write_spec(mic_config_path, STEP_KEY, 6)
    click.secho("Success", fg="green")


@encapsulate.command(short_help="Publish your code in GitHub and your image to DockerHub")
@click.option(
    "-f",
    "--mic_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    default=CONFIG_YAML_NAME
)
@click.option(
    "--profile",
    "-p",
    envvar="MINT_PROFILE",
    type=str,
    default="default",
    metavar="<profile-name>",
)
def step7(mic_file, profile):
    """
    Publish your code and MIC wrapper on GitHub and the Docker Image on DockerHub

    Example:
    mic encapsulate step7 -f <mic_file>
    """
    info_step8()
    mic_config_path = Path(mic_file)
    model_dir = mic_config_path.parent
    click.secho("Deleting the executions")
    push(model_dir, mic_config_path, profile)
    publish_docker(mic_config_path, profile)
    write_spec(mic_config_path, STEP_KEY, 7)


@encapsulate.command(short_help="Publish your model component in the MINT Model Catalog")
@click.option(
    "-f",
    "--mic_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    default=CONFIG_YAML_NAME
)
@click.option(
    "--profile",
    "-p",
    envvar="MINT_PROFILE",
    type=str,
    default="default",
    metavar="<profile-name>",
)
def step8(mic_file, profile):
    """
    Publish your model into the Model Catalog

    Example:
    mic encapsulate step8 -f <mic_file>
    """
    mic_config_path = Path(mic_file)
    model_configuration = create_model_catalog_resource(Path(mic_file), allow_local_path=False)

    api_response_model, api_response_mc = publish_model_configuration(model_configuration, profile)
    click.echo("You can run or see the details using DAME. More info at https://dame-cli.readthedocs.io/en/latest/")
    click.echo("For example, you can run it using:\ndame run {}".format(obtain_id(api_response_mc.id)))
    write_spec(mic_config_path, STEP_KEY, 8)


@encapsulate.command(short_help="Show status")
@click.option(
    "-f",
    "--mic_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    default=CONFIG_YAML_NAME
)
def status(mic_file):
    mic_config_path = Path(mic_file)
    step = get_key_spec(mic_config_path, STEP_KEY)
    click.secho("Step {} of {}".format(step, TOTAL_STEPS))


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
