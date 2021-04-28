import logging
import os
from pathlib import Path
import re
import click
import docker
from docker.errors import APIError
from mic._utils import get_mic_logger
from mic.config_yaml import get_key_spec, write_spec
from mic.constants import DOCKER_KEY, DOCKER_USERNAME_KEY, VERSION_KEY, CONTAINER_NAME_KEY
from mic.credentials import get_credentials

logging = get_mic_logger()


def build_docker(docker_path: Path, name: str):
    client = docker.from_env()
    click.echo("Downloading the base image and building your image")
    logging.info("Downloading and building base docker image")
    try:
        image, logs = client.images.build(path=str(docker_path), tag="{}".format(name), nocache=True)
        for chunk in logs:
            if "stream" in chunk:
                line = chunk["stream"].encode().decode('utf8').replace("\n", "")
                click.echo(f'{line}')
    except docker.errors.BuildError as err:
        click.echo(f'Build Attempt Failed[{name}]')
        logging.warning("Build attempt failed")
        logging.debug(err)
        click.echo(f'{err}')
        for chunk in err.build_log:
            if "stream" in chunk:
                line = chunk["stream"].encode().decode('utf8').replace("\n", "")
                click.echo(f'{line}')
                logging.debug(err)
        raise ValueError
    return image.tags[0]


def publish_docker(mic_config_path, profile):
    # DOCKER_KEY doesn't have the docker username
    docker_image = get_key_spec(mic_config_path, DOCKER_KEY)
    try:
        docker_image = docker_image.split('/')[-1]
    except:
        pass
    try:
        docker_image = docker_image.split(':')[0]
    except:
        pass
    container_name = get_key_spec(mic_config_path, CONTAINER_NAME_KEY)
    docker_username = get_docker_username(profile)
    version = get_key_spec(mic_config_path, VERSION_KEY)
    docker_image_with_version = f"""{docker_username}/{docker_image}:{version}"""
    docker_container_cmd = f"""docker container commit {container_name} {docker_image_with_version} """
    click.secho(f"Committing the changes into the Docker Image "
                f"Please wait...")
    os.system(docker_container_cmd)
    click.secho("Uploading the Docker Image")
    logging.info("Publish docker image")
    try:
        docker_push_cmd = f"""docker push {docker_image_with_version} """
        os.system(docker_push_cmd)
        write_spec(mic_config_path, DOCKER_KEY, docker_image_with_version)

    except Exception as e:
        raise e


def get_docker_username(profile):
    credentials = get_credentials(profile)
    if DOCKER_USERNAME_KEY not in credentials:
        click.secho(
            f"""
Docker username not found.
Please run
$ mic credentials -p {profile}
""")
        exit(0)
    return credentials[DOCKER_USERNAME_KEY]

def image_exists(image_name: str):
    client = docker.from_env()
    try:
        client.images.get(image_name)
    except docker.errors.ImageNotFound:
        click.echo(f"""Image {image_name} not found""")
        exit(1)
    except docker.errors.APIError as e:
        click.echo(f"""Unable to connect with Docker""")
        logging.error(e, exc_info=True)
        exit(1)        

def parse_docker_name(docker_name: str) -> dict:
    username = None
    image_name = None
    version = None
    regex = re.compile("((?P<username>[a-z]+)/)?"
                "(?P<image_name>([a-z0-9]+((?:[._]|__|[-])|[a-z0-9])*))"
                "(:(?P<version>[\w][\w.-]{0,127}))?")
    m = re.search(regex, docker_name)
    username = m.group('username')
    image_name = m.group('image_name')
    version = m.group('version')
    return { 'username': username, 'image_name': image_name, 'version': version}


