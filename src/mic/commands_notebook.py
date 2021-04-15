import os
from pathlib import Path

import click
import semver

import mic
from mic import _utils
from mic._utils import get_mic_logger, check_mic_path, obtain_id
from mic.cli_docs import info_start_publish, info_end_publish
from mic.component.initialization import render_bash_color, render_run_sh, render_io_sh, render_output
from mic.component.reprozip import format_code
from mic.config_yaml import write_to_yaml, get_spec, create_config_file_yaml, write_spec, get_key_spec
from mic.constants import DOCKER_KEY, NAME_KEY

from mic.config_yaml import get_parameters as mic_get_parameters
from mic.config_yaml import get_inputs as mic_get_inputs
from mic.config_yaml import get_outputs_mic as mic_get_outputs

from mic.cwl.cwl import get_parameters, add_parameters, add_outputs, supported, get_base_command, get_docker_image, \
    get_inputs, add_inputs, run, update_docker_image
from mic.publisher.docker import get_docker_username
from mic.publisher.github import push, push_cwl
from mic.publisher.model_catalog import create_model_catalog_resource, publish_model_configuration, \
    create_model_catalog_resource_cwl

from ipython2cwl.repo2cwl import repo2cwl

logging = get_mic_logger()


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



@cli.command(short_help="Expect a cwl definition a values")
@click.argument(
    "url",
    type=click.Path(),
    required=True
)
def read(url):
    repo2cwl([url, "-o", "."])



@cli.command(short_help="Convert CWL Document to ModelCatalog")
@click.argument(
    "spec_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    required=True
)
def transform(spec_file):
    mic_dir = Path(spec_file).parent
    name = str(Path(spec_file).stem)
    mic_config_path = create_config_file_yaml(mic_dir, f"mic_{name}.yaml")
    cwl_spec = get_spec(Path(spec_file))
    write_spec(mic_config_path, NAME_KEY, name)
    supported(cwl_spec)
    cwl_line = get_base_command(cwl_spec)


    parameters = get_parameters(cwl_spec)
    inputs = get_inputs(cwl_spec)
    outputs = cwl_spec["outputs"]
    cwl_values = {}
    for key, item in parameters.items():
        click.secho(f"""Complete information about the input {key}""")
        _type = int
        value = click.prompt(f"""Please enter a valid {item['type']}""", type=_type)
        cwl_values[key] = value
        cwl_line = f"{cwl_line} {item['inputBinding']['prefix']} {cwl_values[key]}"
    
    add_inputs(mic_config_path, inputs, cwl_values)
    add_outputs(mic_config_path, outputs, cwl_values)
    add_parameters(mic_config_path, parameters, cwl_values)
    name = get_key_spec(mic_config_path, NAME_KEY)
    docker_image = get_docker_image(cwl_spec)
    write_spec(mic_config_path, DOCKER_KEY, docker_image)
    write_to_yaml(mic_dir / f"""{name}_values.yaml""", cwl_values)

@cli.command(short_help="Upload the DockerImage")
@click.argument(
    "mic_file",
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
def upload_image(mic_file, profile):
    mic_config_path = Path(mic_file)
    if not mic_config_path.exists():
        exit(1)
    docker_image = get_key_spec(mic_config_path, DOCKER_KEY)
    try:
        docker_username = get_docker_username(profile)
        docker_image_with_version = f"""{docker_username}/{docker_image}:latest"""
        docker_push_cmd = f"""docker tag {docker_image} {docker_image_with_version} && docker push {docker_image_with_version}"""
        os.system(docker_push_cmd)
        write_spec(mic_config_path, DOCKER_KEY, docker_image_with_version)
        update_docker_image(Path(spec_file), docker_image_with_version)
    except Exception as e:
        raise e


@cli.command(short_help="Upload the DockerImage")
@click.argument(
    "mic_file",
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
def upload_configuration(mic_file, profile):
    model_configuration = create_model_catalog_resource_cwl(Path(mic_config_path), name, allow_local_path=False)
    api_response_model, api_response_mc, model_id, software_version_id = publish_model_configuration(model_configuration, profile)
    info_end_publish(obtain_id(model_id), obtain_id(software_version_id), obtain_id(api_response_mc.id),profile)
