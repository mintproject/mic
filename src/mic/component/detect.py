import os
import subprocess
from datetime import datetime
from pathlib import Path

import click
from mic.component.initialization import detect_framework, render_dockerfile, render_conda
from mic.component.python3 import freeze
from mic.constants import DOCKER_DIR, handle, Framework, REQUIREMENTS_FILE, MIC_DIR, REPRO_ZIP_TRACE_DIR


def detect_new_reprozip(src_directory: Path, time: datetime, ignore_dir=[REPRO_ZIP_TRACE_DIR]):
    """
    Get the files by a modification timestamp.
    :param ignore_dir:
    :type ignore_dir:
    :param src_directory: The src execution dir
    :type src_directory: Path
    :param time: Execution time
    :type time: datetime
    """
    files_list = []
    for root, _, filenames in os.walk(src_directory, topdown=True):
        if root.split(os.path.sep)[-1] not in ignore_dir:
            for filename in filenames:
                filepath = os.path.join(os.path.abspath(root), filename)
                file_path = Path(filepath)
                created = os.path.getmtime(file_path)
                modified = os.path.getmtime(file_path)
                if time < created or time < modified:
                    files_list.append(file_path)
    return files_list


def detect_framework_main(user_execution_directory):
    user_execution_directory_mic = user_execution_directory / MIC_DIR
    user_execution_directory_docker = user_execution_directory_mic / DOCKER_DIR
    user_execution_directory_mic.mkdir(exist_ok=True)
    user_execution_directory_docker.mkdir(exist_ok=True)

    frameworks = detect_framework(user_execution_directory)
    click.echo("You can disable the detection of dependencies using the option --no-dependencies ")
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

    extract_dependencies(framework, user_execution_directory_docker)
    dockerfile = render_dockerfile(user_execution_directory_mic, framework)
    click.secho("Dockerfile has been created: {}".format(dockerfile))
    return framework


def extract_dependencies(framework, user_execution_directory_docker):
    if framework == Framework.GENERIC:
        bin_dir = user_execution_directory_docker / "bin"
        bin_dir.mkdir(exist_ok=True)
    elif (framework == Framework.PYTHON37 or framework == Framework.PYTHON38):
        requirements_file = user_execution_directory_docker / REQUIREMENTS_FILE
        freeze(requirements_file)
        click.echo("Extracting the Python dependencies.\nYou can view or edit the dependencies file {} ".format(
            requirements_file))
    # elif framework == Framework.CONDA:
    #     try:
    #         reqs = subprocess.check_output(['conda', 'env', 'export', '--from-history'])
    #         click.echo(reqs)
    #     except:
    #         click.secho("Unable to obtain conda dependencies")
    #     render_conda(user_execution_directory_docker)
