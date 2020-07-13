import logging
import logging
import os
import shutil
from datetime import datetime
from pathlib import Path

import mic
import semver
from mic import _utils
from mic._utils import find_dir, get_filepaths, obtain_id, check_mic_path
from mic.cli_docs import info_start_inputs, info_start_outputs, info_start_wrapper, info_end_inputs, info_end_outputs, \
    info_end_wrapper, info_start_run, info_end_run, info_end_run_failed, info_start_publish, info_end_publish, \
    info_end_publish_dt
from mic.component.detect import detect_framework_main, detect_new_reprozip, extract_dependencies
from mic.component.executor import copy_code_to_src, compress_directory, execute_local, copy_config_to_src
from mic.component.initialization import render_run_sh, render_io_sh, render_output, create_base_directories, \
    render_bash_color, render_dockerfile
from mic.component.reprozip import get_inputs_outputs_reprozip, get_outputs_reprozip, relative, generate_runner, \
    generate_pre_runner, \
    find_code_files
from mic.config_yaml import write_spec, write_to_yaml, get_spec, get_key_spec, create_config_file_yaml, get_configs, \
    get_inputs, get_parameters, get_outputs_mic, get_code, add_params_from_config, get_framework
from mic.constants import *
from mic.publisher.docker import publish_docker, build_docker
from mic.publisher.github import push
from mic.publisher.model_catalog import create_model_catalog_resource, publish_model_configuration, \
    publish_data_transformation, create_data_transformation_resource

logging.basicConfig(level=logging.WARNING)


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
You should consider upgrading via 'pip install --upgrade mic' command.""",
            fg="yellow",
        )


@cli.command(short_help="Create a Linux environment to run your model. The working directory selected must"
                        " contain all the files required for the execution of your model")
@click.argument(
    "user_execution_directory",
    type=click.Path(exists=True, dir_okay=True, file_okay=False, resolve_path=True),
    default=Path('.'),
    required=True
)
@click.option('--name', prompt="Model component name", help="Name of the model component you want for your model")
@click.option('--image',
              help="(Optional) If you have a DockerImage, you can use it",
              default=None)
def start(user_execution_directory, name, image):
    """
    This step generates a mic.yaml file and the directories (data/, src/, docker/). It also initializes a local
    GitHub repository

    The argument: `model_configuration_name` is the name of the model component you are defining in MIC
     """
    user_execution_directory = Path(user_execution_directory)
    mic_dir = user_execution_directory / MIC_DIR
    create_base_directories(mic_dir)
    mic_config_path = create_config_file_yaml(mic_dir)
    if image is None:
        framework = detect_framework_main(user_execution_directory)
    else:
        # If a user provides a image, the framework is generic.
        framework = Framework.GENERIC
        framework.image = image
        render_dockerfile(mic_dir, framework)

    os.system(f"docker pull {framework.image}")
    try:
        user_image = build_docker(mic_dir / DOCKER_DIR, name)
    except ValueError:
        click.secho("The extraction of dependencies has failed", fg='red')
        user_image = framework.image

    write_spec(mic_config_path, NAME_KEY, name)
    write_spec(mic_config_path, DOCKER_KEY, user_image)
    write_spec(mic_config_path, FRAMEWORK_KEY, framework)
    click.secho(f"""
You are in a Linux environment Debian distribution
We detect the following dependencies.

- If you install new dependencies using `apt` or `apt-get`, remember to add them in Dockerfile {Path(MIC_DIR) / DOCKER_DIR / DOCKER_FILE}
- If you install new dependencies using python. Before the step `upload` run

pip freeze > mic/docker/requirements.txt
""", fg="green")
    click.echo("Please, run your Model Component.")
    docker_cmd = f"""docker run --rm -ti \
        --cap-add=SYS_PTRACE \
        -v {user_execution_directory}:/tmp/mint \
        -w /tmp/mint {user_image} """
    print(docker_cmd)
    os.system(docker_cmd)


@cli.command(short_help="Trace any command line and extract the information about your model execution",
             context_settings=dict(
                 ignore_unknown_options=True,
             ))
@click.option('--continue', 'c', is_flag=True, help="add to the previous trace, don't replace it", default=None)
@click.option('--overwrite', 'o', is_flag=True, help="overwrite the previous trace, don't add to it", default=None)
@click.argument('command', nargs=-1, type=click.UNPROCESSED)
def trace(command, c, o):
    """
    Complete the mic.yaml file with the information of the parameters and inputs you want to expose

    MIC is going to automatically detect:
     - All inputs (files and directories) used by your component and add them in the mic.yaml file.
     - All parameters used by your component and add them in the configuration file

    Usage example:
    mic encapsulate trace python main.py
    mic encapsulate trace ./your_program
    """
    if c and o:
        click.secho("You can't use --continue and --overwrite at the same time", fg="red")
        exit(1)

    append = None
    if c:
        append = True
    if o:
        append = False

    import reprozip.tracer.trace
    import reprozip.traceutils
    base_dir = REPRO_ZIP_TRACE_DIR
    base = Path(".") / base_dir
    output_reprozip = base / REPRO_ZIP_CONFIG_FILE

    identify_packages = True
    identify_inputs_outputs = True

    now = datetime.now().timestamp()

    status = reprozip.tracer.trace.trace(command[0], list(command), base_dir, append, 1)
    if status != 0:
        click.secho("Program exited with non-zero code", fg="red")
    reprozip.tracer.trace.write_configuration(base, identify_packages, identify_inputs_outputs, overwrite=False)

    outputs = [str(i.absolute()) for i in detect_new_reprozip(Path("."), now)]
    reprozip_spec = get_spec(output_reprozip)
    reprozip_spec[OUTPUTS_KEY] = reprozip_spec[OUTPUTS_KEY].append(outputs) if OUTPUTS_KEY in reprozip_spec and \
                                                                               reprozip_spec[OUTPUTS_KEY] else outputs
    write_to_yaml(output_reprozip, reprozip_spec)


@cli.command(short_help="Select configuration file(s) for your model (if applicable)")
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
    default=None
)
@click.option('-a', '--auto_param', is_flag=True, default=False, help="Enable automatic detection of parameters")
def configs(mic_file, configuration_files, auto_param):
    """
    Note: If your model does not use configuration files, you can skip this step

    Specify which parameters of your model component you want to expose from any configuration file.

    - You must pass the MIC_FILE (mic.yaml) as an argument using the (-f) option or run the command from the same
    directory as mic.yaml

    - Pass your model configuration files as arguments

    mic encapsulate configs -f <mic_file> [configuration_files]...

    If you have manually changed some parameters, the -a option will attempt to recognize the configuration files
    automatically

    Example:

    mic encapsulate configs -f mic.yaml data/example_dir/file1.txt  data/file2.txt
    """
    # Searches for mic file if user does not provide one
    mic_file = check_mic_path(mic_file)

    mic_config_file = Path(mic_file)
    user_execution_directory = mic_config_file.parent.parent

    if not mic_config_file.exists():
        click.secho("Error: that configuration path does not exist", fg="red")
        exit(1)
    configuration_files = [str(Path(x).absolute()) for x in list(configuration_files)]
    try:
        # Add config file names to yaml
        write_spec(mic_config_file, CONFIG_FILE_KEY, relative(configuration_files, user_execution_directory))
    except Exception as e:
        click.secho("Failed: Error message {}".format(e), fg="red")
    for item in configuration_files:
        click.secho("Added: {} as a configuration file".format(item))
        if auto_param:
            # Parse parameters from config file(s) and add them to mic.yaml
            add_params_from_config(mic_config_file, item)

    write_spec(mic_config_file, STEP_KEY, 2)


@cli.command(short_help="Expose parameters in the " + CONFIG_YAML_NAME + " file", name="parameters")
@click.option('--name', "-n", help="Name of the parameter", required=True, type=click.STRING)
@click.option('--value', "-v", help="Default value of the parameter", required=True, type=ANY_TYPE)
@click.option('--description', "-d", help="Description for parameter", required=False, type=str)
@click.option('--overwrite', "-o", help="Overwrite an existing parameter", is_flag=True, default=False)
@click.option(
    "-f",
    "--mic_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    default=None
)
def add_parameters(mic_file, name, value, overwrite, description):
    """
    Add a parameter into the MIC file (mic.yaml).

    - You must pass the MIC file (mic.yaml) as an argument using the (-f) option; or run the command from the
    same directory as the MIC file (mic.yaml)

    Usage example:

    mic encapsulate parameters -f <mic_file> --name PARAMETER_NAME --value PARAMETER_VALUE
    """
    # Searches for mic file if user does not provide one
    mic_file = check_mic_path(mic_file)

    path = Path(mic_file)
    spec = get_spec(path)

    if PARAMETERS_KEY not in spec:
        spec[PARAMETERS_KEY] = {}

    if not overwrite and name in spec[PARAMETERS_KEY]:
        click.echo("The parameter exists. Add the option --overwrite to overwrite it.")
        exit(1)
    else:

        if description is None:
            description = ""
        type_value____name__ = type(value).__name__
        click.echo(f"Adding the parameter {name}, value {value} and type {type_value____name__}")
        spec[PARAMETERS_KEY].update({name: {DEFAULT_VALUE_KEY: value, DATATYPE_KEY: type_value____name__,
                                            DEFAULT_DESCRIPTION_KEY: description}})
    write_spec(path, PARAMETERS_KEY, spec[PARAMETERS_KEY])


@cli.command(short_help=f"""Expose model inputs into the {CONFIG_YAML_NAME} file""")
@click.argument(
    "custom_inputs",
    type=click.Path(exists=True, dir_okay=True, file_okay=True, resolve_path=True),
    required=False,
    nargs=-1
)
@click.option(
    "-f",
    "--mic_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    default=None
)
def inputs(mic_file, custom_inputs):
    """
Describe the inputs of your model using the information obtained by the `trace` command. To identify  which inputs have
been automatically detected, execute `mic encapsulate inputs -f mic/mic.yaml` and then inspect the mic.yaml file

- You must pass the MIC_FILE (mic.yaml) as an argument using the (-f) option  or run the
command from the same directory as mic.yaml

- Identify undetected files in or directories in mic.yaml and add them as arguments to the `inputs` command

mic encapsulate inputs -f <mic_file> [undetected files]...

Usage example:

mic encapsulate inputs -f mic/mic.yaml input.txt inputs_directory


    """
    # Searches for mic file if user does not provide one
    mic_file = check_mic_path(mic_file)

    info_start_inputs()
    mic_config_file = Path(mic_file)
    mic_directory_path = mic_config_file.parent
    user_execution_directory = mic_config_file.parent.parent
    repro_zip_trace_dir = find_dir(REPRO_ZIP_TRACE_DIR, user_execution_directory)
    repro_zip_trace_dir = Path(repro_zip_trace_dir)
    repro_zip_config_file = repro_zip_trace_dir / REPRO_ZIP_CONFIG_FILE
    spec = get_spec(repro_zip_config_file)
    custom_inputs = [str(user_execution_directory / Path(i).relative_to(user_execution_directory)) for i in
                     list(custom_inputs)]
    inputs_reprozip = get_inputs_outputs_reprozip(spec, user_execution_directory)

    # obtain config: if a file is a config cannot be a input
    config_files = get_configs(mic_config_file)
    config_files_list = [str(user_execution_directory / item[PATH_KEY]) for key, item in
                         config_files.items()] if config_files else []

    code_files = find_code_files(spec, inputs_reprozip, config_files_list, user_execution_directory)
    new_inputs = []
    inputs_reprozip += list(custom_inputs)
    data_dir = mic_directory_path.absolute() / DATA_DIR
    if data_dir.exists():
        shutil.rmtree(data_dir)
    data_dir.mkdir()
    _outputs = get_outputs_reprozip(spec, user_execution_directory)
    for _input in inputs_reprozip:
        item = user_execution_directory / _input
        name = Path(_input).name

        if str(item) in config_files_list or str(item) in code_files or str(item) in _outputs:
            click.secho(f"Ignoring the config {item} as an input.", fg="blue")
        else:
            # Deleting the outputs of the inputs.
            if item.is_dir():
                if sorted([str(i) for i in item.iterdir()]) == sorted(_outputs):
                    click.secho(f"Skipping {item}")
                else:
                    click.secho(f"""Input {name} is a directory""", fg="green")
                    click.secho(f"""Compressing the input {name} """, fg="green")
                    zip_file = compress_directory(item, user_execution_directory)
                    dst_dir = data_dir
                    dst_file = dst_dir / Path(zip_file).name
                    if dst_file.exists():
                        os.remove(dst_file)
                    shutil.move(str(zip_file), str(dst_dir))
                    new_inputs.append(zip_file)
                    click.secho(f"""Input {name}  added """, fg="blue")
            else:
                click.secho(f"""Input {name} is a file""", fg="green")
                new_inputs.append(item)
                dst_file = mic_directory_path / DATA_DIR / str(item.name)
                shutil.copy(item, dst_file)
                click.secho(f"""Input {name}  added """, fg="blue")

    info_end_inputs(new_inputs)
    write_spec(mic_config_file, INPUTS_KEY, relative(new_inputs, user_execution_directory))
    write_spec(mic_config_file, CODE_KEY, relative(code_files, user_execution_directory))


@cli.command(short_help=f"""Expose model outputs in the {CONFIG_YAML_NAME} file""")
@click.argument(
    "custom_outputs",
    type=click.Path(exists=True, dir_okay=True, file_okay=True, resolve_path=True),
    required=False,
    nargs=-1
)
@click.option(
    "-f",
    "--mic_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    default=None
)
def outputs(mic_file, custom_outputs):
    """
  Describe the outputs of your model using the information obtained by the `trace` command.
  To identify  which inputs have been automatically detected, execute `mic encapsulate outputs -f mic/mic.yaml`
  and then inspect the mic.yaml file

  - You must pass the MIC_FILE (mic.yaml) as an argument using the (-f) option; or run the
  command from the same directory as mic.yaml

  - Identify undetected files or directories  in the mic.yaml file and pass them as as arguments to the command

  mic encapsulate outputs -f <mic_file> [undetected files]...

  Example:

  mic encapsulate outputs -f mic/mic.yaml output.txt outputs_directory
    """
    # Searches for mic file if user does not provide one
    mic_file = check_mic_path(mic_file)

    info_start_outputs()
    mic_config_file = Path(mic_file)
    user_execution_directory = mic_config_file.parent.parent
    repro_zip_trace_dir = find_dir(REPRO_ZIP_TRACE_DIR, user_execution_directory)
    repro_zip_trace_dir = Path(repro_zip_trace_dir)
    repro_zip_config_file = repro_zip_trace_dir / REPRO_ZIP_CONFIG_FILE
    spec = get_spec(repro_zip_config_file)
    custom_outputs = [str(user_execution_directory / Path(i).relative_to(user_execution_directory)) for i in
                      list(custom_outputs)]
    outputs = get_outputs_reprozip(spec, user_execution_directory)
    for i in list(custom_outputs):
        if Path(i).is_dir():
            outputs += get_filepaths(i)
        else:
            outputs.append(i)
    for i in outputs:
        click.secho(f"""Output added: {i} """, fg="green")
    info_end_outputs(outputs)
    write_spec(mic_config_file, OUTPUTS_KEY, relative(outputs, user_execution_directory))


@cli.command(
    short_help=f"""Generate the directory structure and commands required to run your model component using the information from the
previous steps""")
@click.option(
    "-f",
    "--mic_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    default=None
)
def wrapper(mic_file):
    """
Generates the MIC Wrapper:a directory structure and commands required to run your model component using the
information gathered from previous steps

  - You must pass the MIC_FILE (mic.yaml) as an argument using the (-f) option or run the
  command from the same directory as mic.yaml

  mic encapsulate wrapper -f <mic_file>

  Example:

  mic encapsulate wrapper -f mic/mic.yaml
    """
    # Searches for mic file if user does not provide one
    mic_file = check_mic_path(mic_file)

    info_start_wrapper()
    mic_config_file = Path(mic_file)
    user_execution_directory = mic_config_file.parent.parent

    repro_zip_trace_dir = find_dir(REPRO_ZIP_TRACE_DIR, user_execution_directory)
    repro_zip_trace_dir = Path(repro_zip_trace_dir)
    repro_zip_config_file = repro_zip_trace_dir / REPRO_ZIP_CONFIG_FILE
    mic_directory_path = mic_config_file.parent

    mic_inputs = get_inputs(mic_config_file)
    mic_parameters = get_parameters(mic_config_file)
    mic_outputs = get_outputs_mic(mic_config_file)
    mic_configs = get_configs(mic_config_file)
    mic_code = get_code(mic_config_file)

    spec = get_spec(mic_config_file)
    reprozip_spec = get_spec(repro_zip_config_file)
    code = f"""{generate_pre_runner(spec, user_execution_directory)}
{generate_runner(reprozip_spec, user_execution_directory, mic_inputs, mic_outputs)}"""
    render_bash_color(mic_directory_path)
    render_run_sh(mic_directory_path, mic_inputs, mic_parameters, mic_outputs, code)
    render_io_sh(mic_directory_path, mic_inputs, mic_parameters, mic_configs)
    render_output(mic_directory_path, mic_outputs, False)
    copy_code_to_src(mic_code, user_execution_directory, mic_directory_path / SRC_DIR)
    copy_config_to_src(mic_configs, user_execution_directory, mic_directory_path / SRC_DIR)
    info_end_wrapper(mic_directory_path / SRC_DIR / RUN_FILE)


@cli.command(short_help=f"""Run your model component with the MIC Wrapper generated in the previous step""")
@click.option(
    "-f",
    "--mic_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    default=None
)
def run(mic_file):
    """
  This step will test the model component you created in previous steps.

  - You must pass the MIC_FILE (mic.yaml) using the option (-f) or run the
  command from the same directory as mic.yaml

  mic encapsulate run -f <mic_file>

  Example:

  mic encapsulate wrapper -f mic/mic.yaml
    """
    # Searches for mic file if user does not provide one
    mic_file = check_mic_path(mic_file)

    execution_name = datetime.now().strftime("%m_%d_%H_%M_%S")
    mic_config_path = Path(mic_file)
    execution_dir = Path(mic_config_path.parent / EXECUTIONS_DIR / execution_name)
    info_start_run(execution_dir.relative_to(mic_config_path.parent.parent))
    if execute_local(mic_config_path, execution_name):
        info_end_run(execution_dir)
        click.echo("You model has passed all the tests. Please, review the outputs files.")
        click.echo('If the model is ok, type "exit" to go back to your computer')
        click.echo('IMPORTANT: type "exit" and then upload your Model Component')
        framework = get_framework(mic_config_path)
        if framework:
            extract_dependencies(framework, mic_config_path.parent / DOCKER_DIR)
    else:
        info_end_run_failed()


@cli.command(
    short_help="Upload your code to GitHub, your image to DockerHub and your model component to the MINT Model Catalog.")
@click.option(
    "-f",
    "--mic_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    default=None
)
@click.option(
    "--profile",
    "-p",
    envvar="MINT_PROFILE",
    type=str,
    default="default",
    metavar="<profile-name>",
)
@click.option('--model_configuration', 'mc', is_flag=True, help="push the component as model configuration",
              default=True)
@click.option('--data_transformation', 'dt', is_flag=True, help="push the component as data transformation",
              default=None)
def upload(mic_file, profile, mc, dt):
    """
  Upload your MIC wrapper (including all the contents of the /src folder) to GitHub, the Docker Image to DockerHub
  and the model component to MINT Model Catalog.

  - You must pass the MIC_FILE (mic.yaml) as an argument using the (-f) option or run the
  command from the same directory as mic.yaml

  mic encapsulate upload -f <mic_file>

  Example:

  mic encapsulate upload -f mic/mic.yaml
    """
    # Searches for mic file if user does not provide one
    if mc and dt:
        mc = False
        dt = True
    mic_file = check_mic_path(mic_file)
    info_start_publish(mc)
    mic_config_path = Path(mic_file)
    name = get_key_spec(mic_config_path, NAME_KEY)
    push(mic_config_path.parent, mic_config_path, name, profile)
    publish_docker(mic_config_path, name, profile)
    if mc:
        model_configuration = create_model_catalog_resource(Path(mic_file), name, allow_local_path=False)
        api_response_model, api_response_mc, model_id, software_version_id = publish_model_configuration(
            model_configuration, profile)
        info_end_publish(obtain_id(model_id), obtain_id(software_version_id), obtain_id(api_response_mc.id), profile)
    elif dt:
        dt_response = create_data_transformation_resource(Path(mic_file), name, allow_local_path=False)
        dt_response = publish_data_transformation(dt_response, profile)
        info_end_publish_dt(None, None, obtain_id(dt_response.id), profile)
