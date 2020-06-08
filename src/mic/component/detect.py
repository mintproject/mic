import click
from mic.component.initialization import detect_framework, render_dockerfile
from mic.component.python3 import freeze
from mic.constants import DOCKER_DIR, handle, Framework, REQUIREMENTS_FILE, MIC_DIR


def detect_framework_main(user_execution_directory):
    user_execution_directory_mic = user_execution_directory / MIC_DIR
    user_execution_directory_docker = user_execution_directory_mic / DOCKER_DIR
    user_execution_directory_mic.mkdir(exist_ok=True)
    user_execution_directory_docker.mkdir(exist_ok=True)
    frameworks = detect_framework(user_execution_directory)
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
        bin_dir = user_execution_directory_docker / "bin"
        bin_dir.mkdir(exist_ok=True)
    elif framework == Framework.PYTHON37:
        requirements_file = user_execution_directory_docker / REQUIREMENTS_FILE
        freeze(requirements_file)
        click.echo("Extracting the Python dependencies.\nYou can view or edit the dependencies file {} ".format(
            requirements_file))
    dockerfile = render_dockerfile(user_execution_directory_mic, framework)
    click.secho("Dockerfile has been created: {}".format(dockerfile))
