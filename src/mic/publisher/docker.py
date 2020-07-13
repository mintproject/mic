from pathlib import Path

import click
import docker
from docker.errors import APIError
from mic.config_yaml import get_key_spec, write_spec
from mic.constants import DOCKER_KEY, DOCKER_USERNAME_KEY, VERSION_KEY, DOCKER_DIR
from mic.credentials import get_credentials


def build_image(mic_config_path, name):
    model_path = mic_config_path.parent
    docker_path = model_path / DOCKER_DIR
    try:
        client = docker.from_env()
        click.echo("Downloading the base image and building your image")
        image, logs = client.images.build(path=str(docker_path), tag="{}".format(name), nocache=True)
        return image.tags[0]
    except APIError as e:
        click.secho("Error building the image", fg="red")
        click.echo(e)
        exit(1)
    except Exception as e:
        click.secho("Error building the image", fg="red")
        click.echo(e)
        exit(1)


def build_docker(docker_path: Path, name: str):
    client = docker.from_env()
    click.echo("Downloading the base image and building your image")
    try:
        image, logs = client.images.build(path=str(docker_path), tag="{}".format(name), nocache=True)
        for chunk in logs:
            if "stream" in chunk:
                line = chunk["stream"].encode().decode('utf8').replace("\n", "")
                click.echo(f'{line}')
    except docker.errors.BuildError as err:
        click.echo(f'Build Attempt Failed[{name}]')
        click.echo(f'{err}')
        for chunk in err.build_log:
            if "stream" in chunk:
                line = chunk["stream"].encode().decode('utf8').replace("\n", "")
                click.echo(f'{line}')
        raise ValueError
    return image.tags[0]


def publish_docker(mic_config_path, image_name, profile):
    version = get_key_spec(mic_config_path, VERSION_KEY)
    write_spec(mic_config_path, DOCKER_KEY, image_name)

    build_image(mic_config_path, image_name)
    credentials = get_credentials(profile)
    click.secho("Uploading the Docker Image")

    try:
        client = docker.from_env()
        if DOCKER_USERNAME_KEY not in credentials:
            exit(0)
        username = credentials[DOCKER_USERNAME_KEY]
        image = client.images.get(image_name)
        image_name_without_version = image_name.split("/")[-1].split(':')[0]
        repository = "{}/{}".format(username, image_name_without_version)
        image.tag(repository, version)
        client.images.push(repository, version)
    except Exception as e:
        raise e
    docker_image = "{}:{}".format(repository, version)
    click.secho("Docker Image: {}".format(docker_image))
    write_spec(mic_config_path, DOCKER_KEY, docker_image)
