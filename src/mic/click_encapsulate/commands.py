import os
from datetime import datetime
from pathlib import Path

import mic
import semver
from mic import _utils
from mic.cli_docs import *
from mic.component.detect import detect_framework_main, detect_news_reprozip
from mic.component.executor import build_docker
from mic.component.initialization import render_run_sh, render_io_sh, render_output
from mic.config_yaml import get_numbers_inputs_parameters, get_inputs_parameters, \
    add_configuration_files, write_spec, write_to_yaml
from mic.constants import *
from modelcatalog import DatasetSpecification, Parameter


@click.group()
@click.option("--verbose", "-v", default=0, count=True)
def cli(verbose):
    _utils.init_logger()
    try:
        lv = ".".join(_utils.get_latest_version().split(".")[:3])
    except Exception as e:
        click.secho(
            f"""WARNING: Unable to check if MIC is updated""",
            fg="yellow",
        )
        return

    cv = ".".join(mic.__version__.split(".")[:3])

    if semver.compare(lv, cv) > 0:
        click.secho(
            f"""WARNING: You are using mic version {mic.__version__}, however version {lv} is available.
You should consider upgrading via the 'pip install --upgrade mic' command.""",
            fg="yellow",
        )


@cli.command(short_help="Set up a MIC directory structure and MIC file template")
@click.argument(
    "user_execution_directory",
    type=click.Path(exists=True, dir_okay=True, file_okay=False, resolve_path=True),
    default=Path('.'),
    required=True
)
@click.option('--dependencies/--no-dependencies', default=True)
def start(user_execution_directory, dependencies):
    """
    Generates mic.yaml and the directories (data/, src/, docker/) for your model component. Also initializes a local
    GitHub repository

    The argument: `model_configuration_name` is the name of your model configuration
     """
    name = "test"
    user_execution_directory = Path(user_execution_directory)
    if dependencies:
        detect_framework_main(user_execution_directory)
    image = build_docker(user_execution_directory / MIC_DIR / DOCKER_DIR, name)
    click.secho(f"""
You are in a Linux environment Debian distribution
We detect the following dependencies.

- If you install new dependencies using `apt` or `apt-get`, remember to add them in Dockerfile {Path(MIC_DIR) / DOCKER_DIR / DOCKER_FILE}
- If you install new dependencies using conda, MIC is going to detect them
- If you install new dependencies using python, MIC is going to detect them
""", fg="green")
    click.echo("Please, run your Model Component.")
    os.system(f"""docker run --rm -ti -v {user_execution_directory}:/tmp/mint -w /tmp/mint {image} bash""")


@cli.command(short_help="Pass the inputs and parameters for your Model Configuration")
@click.argument('command', nargs=-1)
def trace(command):
    """
    Fill the MIC configuration file with the information about the parameters and inputs

    MIC is going to detect:
     - the inputs (files and directory) and add them in the MIC configuration file.
     - the parameters and add them in the configuration file

    Example:
    mic encapsulate trace python main.py
    mic encapsulate trace ./your_program
    """
    import reprozip.tracer.trace
    import reprozip.traceutils
    base_dir = ".reprozip-trace"
    base = Path(".") / base_dir
    identify_packages = True
    identify_inputs_outputs = True

    now = datetime.now().timestamp()

    status = reprozip.tracer.trace.trace(command[0], list(command), base_dir, None, 1)
    reprozip.tracer.trace.write_configuration(base, identify_packages, identify_inputs_outputs, overwrite=False)

    outputs = detect_news_reprozip(Path("."), now)
    output_reprozip = base / "outputs.yaml"
    write_to_yaml(output_reprozip, outputs)
    print(status)
    print(command)


@cli.command(short_help="Create MINT wrapper using the " + CONFIG_YAML_NAME)
@click.option('--add_parameter', type=(str, str))
@click.option('--list_parameter', 'list', flag_value=True)
def parameters(add_parameter, list):
    """
    Create MINT wrapper using the mic.yaml. This command will handle adding inputs and parameters into the run file.

    - You must pass the MIC_FILE (mic.yaml) using the option (-f) or run the command from the same directory as mic.yaml

    Example:
    mic encapsulate step3 -f <mic_file>
    """
    print(add_parameter)
    print(list)


@cli.command(short_help="Select configuration file(s) for your model. If there are any")
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
def config_files(mic_file, configuration_files):
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
