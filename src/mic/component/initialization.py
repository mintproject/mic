import os
from pathlib import Path
import logging
from mic._utils import get_mic_logger
from jinja2 import Environment, PackageLoader, select_autoescape
from mic.constants import *
import platform

env = Environment(
    loader=PackageLoader('mic', 'templates'),
    autoescape=select_autoescape(['html', 'xml']),
    trim_blocks=False,
    lstrip_blocks=False
)

logging = get_mic_logger()


def set_mask(value):
    os.umask(value)


def create_base_directories(mic_component_dir: Path, interactive=True):
    if mic_component_dir.exists():
        click.secho("The directory {} already exists. If you continue, you can lose a previous component".format(
            mic_component_dir.name), fg="yellow")
        logging.info("When creating base dir found base directory already exists: {}".format(
            mic_component_dir))
        if interactive and not click.confirm("Do you want to continue?", default=True, show_default=True):
            logging.info("User aborted initialization")
            click.secho("Initialization aborted", fg="blue")
            exit(0)
    try:
        set_mask(0)
        mic_component_dir.mkdir(exist_ok=True)
    except Exception as e:
        click.secho("Error: {} could not be created".format(
            mic_component_dir), fg="red")
        logging.exception("Could not create base dir: {}".format(mic_component_dir))
        exit(1)

    src = mic_component_dir / SRC_DIR
    docker = mic_component_dir / DOCKER_DIR
    data = mic_component_dir / DATA_DIR
    src.mkdir(parents=True, exist_ok=True)
    docker.mkdir(parents=True, exist_ok=True)
    data.mkdir(parents=True, exist_ok=True)
    logging.info("MIC has initialized the component")
    click.secho("MIC has initialized the component.")
    click.secho("[Created] {}:      {}".format(DATA_DIR, mic_component_dir / DATA_DIR))
    click.secho("[Created] {}:    {}".format(
        DOCKER_DIR, mic_component_dir / DOCKER_DIR))
    click.secho("[Created] {}:       {}".format(SRC_DIR, mic_component_dir / SRC_DIR))
    click.secho("[Created] {}:  {}".format(
        CONFIG_YAML_NAME, mic_component_dir / CONFIG_YAML_NAME))
    return mic_component_dir


def render_gitignore(directory: Path):
    template = env.get_template(GITIGNORE_FILE)
    gitignore_file = directory / GITIGNORE_FILE

    with open(gitignore_file, "w") as gi:
        ignore = render_template(template=template)
        gi.write(ignore)

    gitignore_file.chmod(0o755)
    logging.debug("gitignore rendered")
    return gitignore_file


def render_conda(directory: Path):
    template = env.get_template(CONDA_YML)
    conda = directory / CONDA_YML
    with open(conda, "w") as gi:
        ignore = render_template(template=template)
        gi.write(ignore)
    logging.debug("conda rendered")
    return conda


def render_run_sh(directory: Path,
                  inputs: dict,
                  parameters: dict,
                  outputs: dict,
                  code: str) -> Path:
    """

    @param number_parameters:
    @type number_parameters:
    @param number_inputs:
    @type number_inputs:
    @param directory:
    @type directory:
    @param inputs:
    @type inputs:
    @param parameters:
    @type parameters:
    :param outputs:
    :type outputs:
    """
    template = env.get_template(RUN_FILE)
    run_file = directory / SRC_DIR / RUN_FILE
    number_inputs = len(inputs) if inputs else 0
    number_parameters = len(parameters) if parameters else 0
    number_outputs = len(outputs) if outputs else 0
    with open(run_file, "w") as f:
        content = render_template(template=template,
                                  inputs=inputs,
                                  parameters=parameters,
                                  number_inputs=number_inputs,
                                  number_parameters=number_parameters,
                                  number_outputs=number_outputs,
                                  code=code)
        f.write(content)
    run_file.chmod(0o755)
    logging.debug("run file rendered")
    return run_file


def render_io_sh(directory: Path, inputs: dict, parameters: dict, configs: list) -> Path:
    template = env.get_template(IO_FILE)
    file = directory / SRC_DIR / IO_FILE
    if configs is None:
        configs = []

    list_config = [value[PATH_KEY] for key, value in configs.items()]
    with open(file, "w") as f:
        content = render_template(template=template,
                                  inputs=inputs,
                                  parameters=parameters,
                                  configs=list_config)
        f.write(content)
    logging.debug("io file rendered")
    return file


def detect_framework(src_dir: Path) -> Framework:
    files = {}
    frameworks = [Framework.GENERIC]
    for root, _, filenames in os.walk(src_dir, topdown=True):
        for filename in filenames:
            filepath = Path(os.path.join(os.path.abspath(root), filename))
            if filepath.name not in [RUN_FILE, IO_FILE, OUTPUT_FILE]:
                for name, member in Framework.__members__.items():
                    if member.extension == filepath.suffix and member not in frameworks:
                        frameworks.append(member)
    logging.debug("detecting framework(s): {}".format(frameworks))
    return frameworks


def render_dockerfile(model_directory: Path, language: Framework, custom=False) -> Path:
    template = env.get_template(DOCKER_FILE)
    run_file = model_directory / DOCKER_DIR / DOCKER_FILE

    try:
        os = platform.system().lower()
        logging.debug("OS name: {}".format(os))
    except Exception as e:
        os = "unknown"
        logging.debug("OS name: {}".format(os))
        logging.warning("Error while detecting os: {}".format(e))

    with open(run_file, "w") as f:
        content = render_template(
            template=template, language=language, custom=custom, os=os)

        if os == "windows":
            logging.info("Windows os detected. Converting line endings")

        f.write(content)

    entrypoint_file = model_directory / DOCKER_DIR / ENTRYPOINT_FILE
    template = env.get_template(ENTRYPOINT_FILE)
    with open(entrypoint_file, "w") as f:
        content = render_template(template=template)
        f.write(content)
    # language_tasks(model_directory, language)

    return run_file


def recursive_convert_to_lf(dir):
    """
    Convert windows CRLF endings into unix LF endigns. Returns an array of converted files
    :param dir:
    :return: converted_files
    """
    converted_files = []
    for root, dirs, file_path in os.walk(dir):
        for file in file_path:
            if root.find(".git") == -1:
                with open(Path(root) / Path(file), 'rb') as open_file:
                    content = open_file.read()

                content = content.replace(b'\r\n', b'\n')
                converted_files.append("{}".format(file))

                with open(Path(root) / Path(file), 'wb') as open_file:
                    open_file.write(content)

    return converted_files


def render_bash_color(directory: Path) -> Path:
    template = env.get_template(BASH_COLOR_FILE)
    file = directory / SRC_DIR / BASH_COLOR_FILE
    with open(file, "w") as f:
        content = render_template(template=template)
        f.write(content)
    return file


def render_output(directory: Path, outputs: dict, compress: bool) -> Path:
    template = env.get_template(OUTPUT_FILE)
    run_file = directory / SRC_DIR / OUTPUT_FILE
    files = []
    for key, value in outputs.items():
        files.append(value[PATH_KEY])
    with open(run_file, "w") as f:
        if files and compress:
            content = render_template(template=template, files=files, compress=compress)
        elif files:
            content = render_template(template=template, files=files, compress=None)
        else:
            content = render_template(template=template, files=[], compress=None)
        f.write(content)
    return run_file


def render_template(template, **kwargs):
    return template.render(**kwargs)
