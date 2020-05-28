import click
import docker
from mic.config_yaml import get_key_spec, write_spec
from mic.constants import DOCKER_KEY, DOCKER_USERNAME_KEY, VERSION_KEY
from mic.credentials import get_credentials


def publish_docker(mic_config_path, profile):
    version = get_key_spec(mic_config_path, VERSION_KEY)
    image_name = get_key_spec(mic_config_path, DOCKER_KEY)
    credentials = get_credentials(profile)
    click.secho("Publishing the Docker Image")

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

