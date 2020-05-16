import shutil
from pathlib import Path

import click
from jinja2 import Environment, PackageLoader, select_autoescape

from mic.component.python3 import freeze

RUN_FILE = "run"
IO_FILE = "io.sh"
OUTPUT_FILE = "output.sh"
DOCKER_FILE = "Dockerfile"
SRC_DIR = "src"
DOCKER_DIR = "docker"
DATA_DIR = "data"
REQUIREMENTS_FILE = "requirements.txt"
env = Environment(
    loader=PackageLoader('mic', 'templates'),
    autoescape=select_autoescape(['html', 'xml']),
    trim_blocks=False,
    lstrip_blocks=False
)


def create_directory(parent_directory: Path, name: str):
    parent_directory = parent_directory / name
    if parent_directory.exists():
        shutil.rmtree(parent_directory)
    src = parent_directory / SRC_DIR
    docker = parent_directory / DOCKER_DIR
    data = parent_directory / DATA_DIR
    src.mkdir(parents=True)
    docker.mkdir(parents=True)
    data.mkdir(parents=True)
    click.secho("Created: {}".format(src.absolute()), fg="green")
    click.secho("Created: {}".format(docker.absolute()), fg="green")
    click.secho("Created: {}".format(data.absolute()), fg="green")
    return parent_directory


def render_run_sh(directory: Path,
                  inputs: dict, parameters: dict,
                  number_inputs: int = 0, number_parameters: int = 0) -> Path:
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
    """
    template = env.get_template(RUN_FILE)
    run_file = directory / SRC_DIR / RUN_FILE
    with open(run_file, "w") as f:
        content = render_template(template=template, inputs=inputs, parameters=parameters,
                                  number_inputs=number_inputs, number_parameters=number_parameters, number_outputs=0)
        f.write(content)
    return run_file


def render_io_sh(directory: Path) -> Path:
    template = env.get_template(IO_FILE)
    run_file = directory / SRC_DIR / IO_FILE
    with open(run_file, "w") as f:
        content = render_template(template=template)
        f.write(content)
    return run_file


def render_dockerfile(directory: Path, language: str) -> Path:
    template = env.get_template(DOCKER_FILE)
    run_file = directory / DOCKER_DIR / DOCKER_FILE
    with open(run_file, "w") as f:
        content = render_template(template=template, language=language)
        f.write(content)
    language_tasks(directory, language)
    return run_file


def language_tasks(directory, language):
    if language == "python3":
        run_file = directory / DOCKER_DIR / REQUIREMENTS_FILE
        freeze(run_file)


def render_template(template, **kwargs):
    return template.render(**kwargs)
