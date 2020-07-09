import click
import validators
from mic.constants import MODEL_CATALOG_URL
from validators import ValidationFailure


def info_start_inputs():
    click.secho("Detecting the data of your model using the information obtained by the `trace` command.", fg="blue")
    click.secho("Creating the inputs.", fg="blue")
    click.secho("If the data is a directory, MIC is going to compress in a zipfile.", fg="blue")


def info_end_inputs(inputs):
    click.secho("Success", fg="green")
    click.secho("The inputs of model component are available in the mic directory. ", fg="blue")
    click.secho(f"You model component has {len(inputs)} inputs", fg="blue")
    click.secho("The next step is `mic encapsulate outputs`")
    click.secho(
        "MIC is going to detect the outputs of your model using the information obtained by the `trace` command.")
    click.secho("For more information, you can type.")
    click.secho("mic encapsulate outputs --help")


def info_start_outputs():
    click.secho("Detecting the output of your model using the information obtained by the `trace` command.", fg="blue")


def info_end_outputs(outputs):
    click.secho("Success", fg="green")
    click.secho(f"You model component has {len(outputs)} outputs", fg="blue")
    click.secho("The next step is `mic encapsulate wrapper`")
    click.secho("MIC is going to generate the directory structure and commands required to run your model.")
    click.secho("For more information, you can type.")
    click.secho("mic encapsulate wrapper --help")


def info_start_wrapper():
    click.secho(
        "Generating the MIC Wrapper. This generates the directory structure and commands required to run your model",
        fg="blue")


def info_end_wrapper(run):
    click.secho("Success", fg="green")
    click.secho(f"The wrapper has been generated. You can see it at {run}", fg="blue")
    click.secho("The next step is `mic encapsulate run`")
    click.secho("The command run is going to create a new directory (execution directory), "
                "and MIC is going the inputs, code, and configuration files and run the model.")
    click.secho("For more information, you can type.")
    click.secho("mic encapsulate run --help")


def info_start_run(execution_dir):
    if not click.confirm(
            f"MIC needs to create new directory {execution_dir} to run the model component "
            "Do you want to continue", default=True):
        exit(0)


def info_end_run(execution_dir):
    click.secho("Success", fg="green")
    click.secho(f"You can see the result at {execution_dir}", fg="blue")
    click.secho("The next step is `mic encapsulate upload`")
    click.secho("The step is going to upload the MIC Wrapper to GitHub, "
                "the DockerImage on DockerHub and the Model Configuration on the MINT Model Catalog")


def info_end_run_failed():
    click.secho("Failed", fg="red")
    click.secho(f"Something is wrong. You can report this problem at https://bit.ly/2zR1Tew", fg="blue")


def info_start_publish(mc):
    resource = "Model Configuration" if mc else "Data Transformation"
    click.echo(f"This step publishes your code, DockerImage and {resource}")


def info_end_publish_dt(model_id, model_version_id, model_configuration_id, profile):
    click.secho("Success", fg="green")
    if model_id and model_version_id and model_configuration_id:
        click.secho("You can edit the metadata using the MINT-UI")
        url = f"{MODEL_CATALOG_URL}/{model_id}/{model_version_id}/{model_configuration_id}"
        try:
            if validators.url(url):
                click.secho(url)
        except ValidationFailure as e:
            click.secho("Unable to generate the public url")
            exit(1)
    click.echo("You can run the Model using DAME")
    click.echo(f"dame run {model_configuration_id} -p {profile}")


def info_end_publish(model_id, model_version_id, model_configuration_id, profile):
    click.secho("Success", fg="green")
    if model_id and model_version_id and model_configuration_id:
        click.secho("You can edit the metadata using the MINT-UI")
        url = f"{MODEL_CATALOG_URL}/{model_id}/{model_version_id}/{model_configuration_id}"
        try:
            if validators.url(url):
                click.secho(url)
        except ValidationFailure as e:
            click.secho("Unable to generate the public url")
            exit(1)
    click.echo("You can run the Model using DAME")
    click.echo(f"dame run {model_configuration_id} -p {profile}")
