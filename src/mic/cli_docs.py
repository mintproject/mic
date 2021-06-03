import click
import validators
import logging
from mic._utils import get_mic_logger
from mic.constants import MODEL_CATALOG_URL
from validators import ValidationFailure

logging = get_mic_logger()

def info_start_inputs():
    click.secho("Detecting the data of your model using the information obtained by the `trace` command.", fg="green")
    click.secho("Creating the inputs.")
    click.secho("If the data is a directory, MIC is going to compress in a zipfile.")


def info_end_inputs(inputs):
    click.secho("Success", fg="green")
    click.secho("The inputs of model component are available in the mic directory. ", fg="green")
    click.secho(f"You model component has {len(inputs)} inputs", fg="green")
    click.secho("The next step is `mic pkg outputs`")
    click.secho(
        "MIC is going to detect the outputs of your model using the information obtained by the `trace` command.")
    click.secho("For more information, you can type.")
    click.secho("mic pkg outputs --help")


def info_start_outputs():
    click.secho("Detecting the output of your model using the information obtained by the `trace` command.", fg="green")


def info_end_outputs(outputs):
    click.secho("Success", fg="green")
    click.secho(f"You model component has {len(outputs)} outputs", fg="green")
    click.secho("The next step is `mic pkg wrapper`")
    click.secho("MIC is going to generate the directory structure and commands required to run your model.")
    click.secho("For more information, you can type.")
    click.secho("mic pkg wrapper --help")


def info_start_wrapper():
    click.secho(
        "Generating the MIC Wrapper. This generates the directory structure and commands required to run your model",
        fg="blue")


def info_end_wrapper(run):
    click.secho("Success", fg="green")
    click.secho(f"The wrapper has been generated. You can see it at {run}", fg="blue")
    click.secho("The next step is `mic pkg run`")
    click.secho("The command run is going to create a new directory (execution directory), "
                "and MIC is going the inputs, code, and configuration files and run the model.")
    click.secho("For more information, you can type.")
    click.secho("mic pkg run --help")


def info_start_run(execution_dir):
    if not click.confirm(
            f"MIC needs to create new directory {execution_dir} to run the model component "
            "Do you want to continue", default=True):
        logging.info("User aborted run")
        exit(0)


def info_end_run(execution_dir):
    click.secho("Success", fg="green")
    click.secho(f"You can see the result at {execution_dir}", fg="blue")
    click.secho("The next step is `mic pkg upload`")
    click.secho("The step is going to upload the MIC Wrapper, "
                "the DockerImage on DockerHub and the Model Configuration on the MINT Model Catalog")


def info_end_run_failed():
    click.secho("Failed", fg="red")
    click.secho("Something is wrong. You can report this problem at https://bit.ly/2zR1Tew", fg="blue")


def info_start_publish(mc = True):
    resource = "Model Configuration" if mc else "Data Transformation"
    click.echo(f"This step publishes your code, DockerImage and {resource}")


def info_end_publish_dt(model_id, model_version_id, model_configuration_id, profile):
    click.secho("Success", fg="green")
    click.echo("You can run the Model using DAME")
    click.echo(f"dame run {model_configuration_id} -p {profile}")


def info_end_publish(model_id, model_version_id, model_configuration_id, profile):
    click.secho("Success", fg="green")
    click.echo("You can run the Model using DAME")
    click.echo(f"dame run {model_configuration_id} -p {profile}")
