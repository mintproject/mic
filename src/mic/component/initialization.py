import shutil
from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape

RUN_FILE = "run"
IO_FILE = "io.sh"
DOCKER_FILE = "Dockerfile"
SRC_DIR = "src"
DOCKER_DIR = "docker"

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
    src.mkdir(parents=True)
    docker.mkdir(parents=True)
    return parent_directory


def render_run_sh(directory: Path, inputs: int = 0, parameters: int = 0, outputs: int = 0, language="generic") -> Path:
    """

    @param language:
    @type language:
    @param directory:
    @type directory:
    @param inputs:
    @type inputs:
    @param parameters:
    @type parameters:
    @param outputs:
    @type outputs:
    """
    template = env.get_template(RUN_FILE)
    run_file = directory / SRC_DIR / RUN_FILE
    with open(run_file, "w") as f:
        content = render_template(template=template, inputs=inputs, outputs=outputs, parameters=parameters)
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
        content = render_template(template=template)
        f.write(content)
    return run_file


def render_template(template, **kwargs):
    return template.render(**kwargs)
