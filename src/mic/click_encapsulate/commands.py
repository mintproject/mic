import ast
import os
import shutil
from datetime import datetime
from pathlib import Path

import click
import mic
import semver
from mic import _utils
from mic._utils import find_dir
from mic.component.detect import detect_framework_main, detect_new_reprozip
from mic.component.executor import copy_code_to_src, compress_directory, execute_local
from mic.component.initialization import render_run_sh, render_io_sh, render_output, create_base_directories
from mic.component.reprozip import get_inputs, get_outputs, relative, generate_runner, generate_pre_runner, \
    find_code_files
from mic.config_yaml import write_spec, write_to_yaml, get_spec, get_key_spec, create_config_file_yaml
from mic.constants import *
from mic.publisher.docker import publish_docker, build_docker
from mic.publisher.github import push
from mic.publisher.model_catalog import create_model_catalog_resource, publish_model_configuration


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


@cli.command(short_help="Create a Linux environment. The working directory must contains all the files required in the"
                        " execution")
@click.argument(
    "user_execution_directory",
    type=click.Path(exists=True, dir_okay=True, file_okay=False, resolve_path=True),
    default=Path('.'),
    required=True
)
@click.option('--dependencies/--no-dependencies', default=True)
@click.option('--name', prompt="Model Configuration name")
def start(user_execution_directory, dependencies, name):
    """
    Generates mic.yaml and the directories (data/, src/, docker/) for your model component. Also initializes a local
    GitHub repository

    The argument: `model_configuration_name` is the name of your model configuration
     """
    user_execution_directory = Path(user_execution_directory)
    mic_dir = user_execution_directory / MIC_DIR
    create_base_directories(mic_dir)
    mic_config_path = create_config_file_yaml(mic_dir)
    framework = detect_framework_main(user_execution_directory, dependencies)
    image = build_docker(mic_dir / DOCKER_DIR, name)
    if not image:
        click.secho("The extraction of dependencies has failed", fg='red')
        click.secho("Running a Docker Container without your dependencies. Please install them manually", fg='green')
        image = framework.image
    write_spec(mic_config_path, NAME_KEY, name)
    click.secho(f"""
You are in a Linux environment Debian distribution
We detect the following dependencies.

- If you install new dependencies using `apt` or `apt-get`, remember to add them in Dockerfile {Path(MIC_DIR) / DOCKER_DIR / DOCKER_FILE}
- If you install new dependencies using python. Before the step `publish` run

pip freeze > mic/docker/requirements.txt
""", fg="green")
    click.echo("Please, run your Model Component.")
    os.system(
        f"""docker run --rm -ti --cap-add=SYS_PTRACE -v {user_execution_directory}:/tmp/mint -w /tmp/mint {image} bash""")


@cli.command(short_help="Trace any command line and extract the information about the execution",
             context_settings=dict(
                ignore_unknown_options=True,
            ))
@click.option('--continue/--overwrite', 'append', default=None)
@click.argument('command', nargs=-1, type=click.UNPROCESSED)
def trace(command, append):
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
    base_dir = REPRO_ZIP_TRACE_DIR
    base = Path(".") / base_dir
    output_reprozip = base / REPRO_ZIP_CONFIG_FILE

    identify_packages = True
    identify_inputs_outputs = True

    now = datetime.now().timestamp()

    status = reprozip.tracer.trace.trace(command[0], list(command), base_dir, append, 1)
    reprozip.tracer.trace.write_configuration(base, identify_packages, identify_inputs_outputs, overwrite=False)

    outputs = [str(i.absolute()) for i in detect_new_reprozip(Path("."), now)]
    reprozip_spec = get_spec(output_reprozip)
    reprozip_spec[OUTPUTS_KEY] = reprozip_spec[OUTPUTS_KEY].append(outputs) if OUTPUTS_KEY in reprozip_spec and \
                                                                               reprozip_spec[OUTPUTS_KEY] else outputs
    write_to_yaml(output_reprozip, reprozip_spec)


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
def configs(mic_file, configuration_files):
    """
    If your model does not use configuration files, you can skip this step

    Specify the inputs and parameters of your model component from configuration file(s)

    - You must pass the MIC_FILE (mic.yaml) using the option (-f) or run the command from the same directory as mic.yaml

    - Pass the configuration files as arguments

    mic encapsulate configs -f <mic_file> [configuration_files]...

    Example:

    mic encapsulate configs -f mic.yaml data/example_dir/file1.txt  data/file2.txt
    """
    mic_config_file = Path(mic_file)
    user_execution_directory = mic_config_file.parent.parent

    if not mic_config_file.exists():
        click.secho("Error: that configuration path does not exist", fg="red")
        exit(1)
    configuration_files = [str(Path(x).absolute()) for x in list(configuration_files)]
    try:
        write_spec(mic_config_file, CONFIG_FILE_KEY, relative(configuration_files, user_execution_directory))
    except Exception as e:
        click.secho("Failed: Error message {}".format(e), fg="red")
    for item in configuration_files:
        click.secho("Added: {} as a configuration file".format(item))
    write_spec(mic_config_file, STEP_KEY, 2)


@cli.command(short_help="Add parameters " + CONFIG_YAML_NAME, name="parameters")
@click.argument("name", required=True, type=str)
@click.argument("value", required=True)
@click.option(
    "-f",
    "--mic_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    default=CONFIG_YAML_NAME
)
def add_parameters(mic_file, name, value):
    """
    Add a parameter into the MIC file (mic.yaml).

    - You must pass the MIC_FILE (mic.yaml) using the option (-f) or run the command from the same directory as mic.yaml

    Example:

    mic encapsulate parameters -f <mic_file> PARAMETER_NAME PARAMETER_VALUE
    """
    path = Path(mic_file)
    spec = get_spec(path)
    if PARAMETERS_KEY not in spec:
        spec[PARAMETERS_KEY] = {}

    if name in spec[PARAMETERS_KEY]:
        click.echo("The parameter exists")
    else:
        spec[PARAMETERS_KEY].update({name: {DEFAULT_VALUE_KEY: ast.literal_eval(value)}})
    write_spec(path, PARAMETERS_KEY, spec[PARAMETERS_KEY])


@cli.command(short_help=f"""Write inputs into {CONFIG_YAML_NAME}""")
@click.argument(
    "custom_inputs",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    required=False,
    nargs=-1
)
@click.option(
    "-f",
    "--mic_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    default=CONFIG_YAML_NAME
)
def inputs(mic_file, custom_inputs):
    mic_config_file = Path(mic_file)
    mic_directory_path = mic_config_file.parent
    user_execution_directory = mic_config_file.parent.parent
    repro_zip_trace_dir = find_dir(REPRO_ZIP_TRACE_DIR, user_execution_directory)
    repro_zip_trace_dir = Path(repro_zip_trace_dir)
    repro_zip_config_file = repro_zip_trace_dir / REPRO_ZIP_CONFIG_FILE
    spec = get_spec(repro_zip_config_file)
    custom_inputs = [str(user_execution_directory / Path(i).relative_to(user_execution_directory)) for i in
                     list(custom_inputs)]
    inputs = get_inputs(spec, user_execution_directory) + list(custom_inputs)

    #obtain config: if a file is a config cannot be a input
    config_files = get_key_spec(mic_config_file, CONFIG_FILE_KEY)
    config_files = [str(user_execution_directory / item[PATH_KEY]) for key, item in config_files.items()] if config_files else []


    code_files = find_code_files(spec, inputs, config_files)
    new_inputs = []

    for _input in inputs:
        item = user_execution_directory / _input
        if str(item) in config_files or str(item) in code_files:
            click.secho(f"Ignoring the config {item} as a input.", fg="blue")
        else:
            if item.is_dir():
                click.secho(f"""Compressing the input {_input} """, fg="blue")
                zip_file = compress_directory(item)
                dst_dir = mic_directory_path.absolute() / DATA_DIR
                new_inputs.append(zip_file)
                dst_file = dst_dir / Path(zip_file).name
                if dst_file.exists():
                    os.remove(dst_file)
                shutil.move(zip_file, dst_dir)
            else:
                new_inputs.append(item)
                dst_file = mic_directory_path / DATA_DIR / str(item.name)
                shutil.copy(item, dst_file)
            click.secho(f"""Input added: {dst_file} """, fg="green")

    # Obtain config files
    # A config file cannot be a input

    click.secho('Writing inputs metadata', fg="blue")
    write_spec(mic_config_file, INPUTS_KEY, relative(new_inputs, user_execution_directory))
    write_spec(mic_config_file, CODE_KEY, relative(code_files, user_execution_directory))

@cli.command(short_help=f"""Write outputs into {CONFIG_YAML_NAME}""")
@click.argument(
    "custom_outputs",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    required=False,
    nargs=-1
)
@click.option('--aggregate/--no-aggregate', default=False)
@click.option(
    "-f",
    "--mic_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    default=CONFIG_YAML_NAME
)
def outputs(mic_file, aggregate, custom_outputs):
    mic_config_file = Path(mic_file)
    user_execution_directory = mic_config_file.parent.parent
    repro_zip_trace_dir = find_dir(REPRO_ZIP_TRACE_DIR, user_execution_directory)
    repro_zip_trace_dir = Path(repro_zip_trace_dir)
    repro_zip_config_file = repro_zip_trace_dir / REPRO_ZIP_CONFIG_FILE
    spec = get_spec(repro_zip_config_file)
    custom_outputs = [str(user_execution_directory / Path(i).relative_to(user_execution_directory)) for i in
                      list(custom_outputs)]
    outputs = get_outputs(spec, user_execution_directory, aggregrate=aggregate) + list(custom_outputs)
    click.secho('Writing output metadata', fg="blue")
    for i in outputs:
        click.secho(f"""Output added: {i} """, fg="green")
    write_spec(mic_config_file, OUTPUTS_KEY, relative(outputs, user_execution_directory))


@cli.command(short_help=f"""Run the wrapper {CONFIG_YAML_NAME}""")
@click.option(
    "-f",
    "--mic_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    default=CONFIG_YAML_NAME
)
def wrapper(mic_file):
    mic_config_file = Path(mic_file)
    user_execution_directory = mic_config_file.parent.parent

    repro_zip_trace_dir = find_dir(REPRO_ZIP_TRACE_DIR, user_execution_directory)
    repro_zip_trace_dir = Path(repro_zip_trace_dir)
    repro_zip_config_file = repro_zip_trace_dir / REPRO_ZIP_CONFIG_FILE
    mic_directory_path = mic_config_file.parent

    parameters = get_key_spec(mic_config_file, PARAMETERS_KEY)
    inputs = get_key_spec(mic_config_file, INPUTS_KEY)
    outputs = get_key_spec(mic_config_file, OUTPUTS_KEY)
    configs = get_key_spec(mic_config_file, CONFIG_FILE_KEY)


    inputs = inputs if inputs else []
    outputs = outputs if outputs else []
    configs = configs if configs else []


    spec = get_spec(mic_config_file)
    reprozip_spec = get_spec(repro_zip_config_file)
    code = f"""{generate_pre_runner(spec, user_execution_directory)}
{generate_runner(reprozip_spec, user_execution_directory)}"""
    write_spec(mic_config_file, COMMANDS_RUNNER, code)
    render_run_sh(mic_directory_path, inputs, parameters, outputs, code)
    render_io_sh(mic_directory_path, inputs, parameters, configs)
    render_output(mic_directory_path, [], False)
    copy_code_to_src(get_key_spec(mic_config_file, CODE_KEY), user_execution_directory, mic_directory_path / SRC_DIR)
    copy_code_to_src(get_key_spec(mic_config_file, CONFIG_FILE_KEY), user_execution_directory, mic_directory_path / SRC_DIR)


@cli.command(short_help=f"""Run the wrapper {CONFIG_YAML_NAME}""")
@click.option(
    "-f",
    "--mic_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    default=CONFIG_YAML_NAME
)
def run(mic_file):
    execute_local(Path(mic_file))


@cli.command(short_help="Publish your code in GitHub and your image to DockerHub")
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
def publish(mic_file, profile):
    """
    Publish your code and MIC wrapper on GitHub and the Docker Image on DockerHub
    Example:
    mic encapsulate step7 -f <mic_file>
    """
    mic_config_path = Path(mic_file)
    name = get_key_spec(mic_config_path, NAME_KEY)

    click.secho("Deleting the executions")
    push(mic_config_path.parent, mic_config_path, name, profile)
    publish_docker(mic_config_path, name, profile)
    model_configuration = create_model_catalog_resource(Path(mic_file), name, allow_local_path=False)
    api_response_model, api_response_mc = publish_model_configuration(model_configuration, profile)
    print(api_response_mc.id)
