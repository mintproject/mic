import docker
from mic.config_yaml import get_key_spec
from mic.constants import DOCKER_KEY, DOCKER_USERNAME_KEY
from mic.credentials import get_credentials


def publish_docker(mic_config_path, profile, version):
    image_name = get_key_spec(mic_config_path, DOCKER_KEY)
    credentials = get_credentials(profile)
    try:
        client = docker.from_env()
        if DOCKER_USERNAME_KEY not in credentials:
            exit(0)
        username = credentials[DOCKER_USERNAME_KEY]
        image = client.images.get(image_name)
        image_name_without_version = image_name.split(":")[0]
        repository = "{}/{}".format(username, image_name_without_version)
        image.tag(repository, version)
        client.images.push(repository, version)
    except Exception as e:
        raise e
    return "{}/{}".format(repository, version)