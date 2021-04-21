#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Implementation for the notebook commands.
"""
import os
from pathlib import Path
import tempfile
import click
import semver
from datetime import datetime

from ipython2cwl.repo2cwl import repo2cwl
from cwltool.main import run as cwltool_run
import mic
from mic import _utils
from mic._utils import get_mic_logger, obtain_id
from mic.cli_docs import info_start_publish, info_end_publish
from mic.config_yaml import get_spec, write_spec, get_key_spec
from mic.constants import DOCKER_KEY, NAME_KEY
from mic.cwl.cwl import add_parameters, add_outputs, get_docker_image, \
    add_inputs, update_docker_image
from mic.publisher.docker import get_docker_username, image_exists
from mic.publisher.model_catalog import publish_model_configuration, \
    create_model_catalog_resource_cwl


logging = get_mic_logger()


@click.group()
@click.option("--verbose", "-v", default=0, count=True)
def cli(verbose):
    """Check if the user is using the latest version

    Args:
        verbose (int): Log level
    """
    if verbose:
        pass
    _utils.init_logger()
    try:
        latest_version = ".".join(_utils.get_latest_version().split(".")[:3])
    except Exception as e:
        click.secho(
            """WARNING: Unable to check if MIC is updated""",
            fg="yellow",
        )
        logging.debug(e, exc_info=True)
        return

    current_version = ".".join(mic.__version__.split(".")[:3])

    if semver.compare(latest_version, current_version) > 0:
        click.secho(
            f"""WARNING: You are using mic version {mic.__version__}, however version
            {latest_version} is available. You should consider upgrading via
            pip install --upgrade mic' command.""",
            fg="yellow",
        )


@cli.command(short_help="Clone your repository, build the image and generate a Model Component.")
@click.argument(
    "url",
    type=click.Path(),
    required=True
)
def read(url):
    """Use repo2cwl to clone the repository and build it

    Args:
        url ([type]): [description]
    """
    repo2cwl([url, "-o", "."])


@cli.command(short_help="Run and test your Model Compoent")
@click.argument(
    "cwl_document",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    required=True
)
@click.argument(
    "cwl_values",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    required=True
)
def run(cwl_document, cwl_values):
    cwltool_run([cwl_document, cwl_values])


@cli.command(short_help="Upload the DockerImage")
@click.argument(
    "cwl_document",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    required=True
)
@click.option(
    "--profile",
    "-p",
    envvar="MINT_PROFILE",
    type=str,
    default="default",
    metavar="<profile-name>",
    help="specify a profile to list"
)
def upload_image(cwl_document, profile):
    cwl_path = Path(cwl_document)
    if not cwl_path.exists():
        exit(1)    
    #Get the cwl spec
    cwl_spec = get_spec(cwl_path)
    try:
        docker_image = get_docker_image(cwl_spec)
    except ValueError as e:
        click.secho(f"""Unable to find image, please verify the {cwl_document}""")
        exit(1)
    image_exists(docker_image)
    click.echo(f"""Image {docker_image} detected""")
    #Get the DockerUsername from crendentials
    docker_username = get_docker_username(profile)
    click.echo(f"""Docker username detected: {docker_username}""")
    #Generate a unique version from the time
    version = datetime.now().strftime("%Y%m%d-%H%M%S")
    docker_image_with_version = f"""{docker_username}/{docker_image}:{version}"""
    docker_push_cmd = f"""docker tag {docker_image} {docker_image_with_version} && docker push {docker_image_with_version}"""
    try:
        os.system(docker_push_cmd)
    except Exception as e:
        click.echo('Unable to push the image')
        exit(1)
        raise e

    write_spec(cwl_path, DOCKER_KEY, docker_image_with_version)
    update_docker_image(cwl_path, docker_image_with_version)

@cli.command(short_help="Upload the Component")
@click.argument(
    "cwl_document",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    required=True
)
@click.argument(
    "cwl_values",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    required=True
)
@click.option(
    "--profile",
    "-p",
    envvar="MINT_PROFILE",
    type=str,
    default=None,
    metavar="<profile-name>",
    help="specify a profile to list"
)
def upload_configuration(cwl_document, cwl_values, profile):
    # create a temporal file
    mic_config_path = tempfile.NamedTemporaryFile(suffix=".yml", prefix="mic")
    # get the name from cwl document and write
    name = Path(cwl_document).stem
    write_spec(mic_config_path, NAME_KEY, name)
    # read the CWL document and stored as dict
    cwl_document_dict = get_spec(cwl_document)
    # get the input, parameters and outputs from cwl and create MIC file
    add_inputs(mic_config_path, cwl_document_dict, cwl_values)
    add_outputs(mic_config_path, cwl_document_dict, cwl_values)
    add_parameters(mic_config_path, cwl_document_dict, cwl_values)
    # obtain the docker image from cwl
    docker_image = get_docker_image(cwl_document)
    write_spec(mic_config_path, DOCKER_KEY, docker_image)

    # Message publish start
    info_start_publish(True)
    # push the component
    model_configuration = create_model_catalog_resource_cwl(
        Path(mic_config_path),
        name,
        allow_local_path=False
    )
    api_response_model, api_response_mc, model_id, software_version_id = publish_model_configuration(
        model_configuration, profile)
    # Message publish end
    info_end_publish(obtain_id(model_id),
                     obtain_id(software_version_id),
                     obtain_id(api_response_mc.id),
                     profile
                     )