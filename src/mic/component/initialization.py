import shutil
from pathlib import Path
from typing import List

import click
from jinja2 import Environment, PackageLoader, select_autoescape
from mic.component.python3 import freeze
from mic.constants import *

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


def render_gitignore(directory: Path):
    template = env.get_template(GITIGNORE_FILE)
    gitignore_file = directory / GITIGNORE_FILE

    with open(gitignore_file, "w") as gi:
        ignore = render_template(template=template)
        gi.write(ignore)

    gitignore_file.chmod(0o755)
    click.secho("Created: {}".format(gitignore_file.absolute()), fg="green")
    return gitignore_file


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
    run_file.chmod(0o755)
    return run_file


def render_io_sh(directory: Path, inputs: dict, parameters: dict, configs: list) -> Path:
    template = env.get_template(IO_FILE)
    data_dir = directory / DATA_DIR
    run_file = directory / SRC_DIR / IO_FILE
    with open(run_file, "w") as f:
        content = render_template(template=template, inputs=inputs,
                                  parameters=parameters, configs=[str(Path(directory / i).relative_to(data_dir)) for i in configs])
        f.write(content)
    return run_file


def detect_framework(src_dir: Path) -> Framework:
    return None


def render_dockerfile(model_directory: Path, language: Framework) -> Path:
    template = env.get_template(DOCKER_FILE)
    run_file = model_directory / DOCKER_DIR / DOCKER_FILE
    with open(run_file, "w") as f:
        content = render_template(template=template, language=language)
        f.write(content)
    # language_tasks(model_directory, language)
    return run_file


def render_output(directory: Path, files: List[Path], compress: str) -> Path:
    template = env.get_template(OUTPUT_FILE)
    run_file = directory / SRC_DIR / OUTPUT_FILE
    with open(run_file, "w") as f:
        if files and compress:
            content = render_template(template=template, files=files, compress=compress)
        elif files:
            content = render_template(template=template, files=files, compress=None)
        else:
            content = render_template(template=template, files=[], compress=None)
        f.write(content)
    return run_file


def language_tasks(directory, language):
    if language == "python3":
        run_file = directory / DOCKER_DIR / REQUIREMENTS_FILE
        freeze(run_file)


def render_template(template, **kwargs):
    return template.render(**kwargs)
