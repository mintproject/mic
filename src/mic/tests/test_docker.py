from pathlib import Path

from mic.config_yaml import get_spec
from mic.cwl.cwl import get_parameters
from mic.publisher.docker import parse_docker_name
RESOURCES = "resources"

def test_get_docker():
    names = {
        'user/name:version': {
            'image_name': 'name',
            'username': 'user',
            'version': 'version'
        },
        'name:version': {
            'image_name': 'name',
            'username': None,
            'version': 'version'
        },
        'name': {
            'image_name': 'name',
            'username': None,
            'version': None
        }
    }


    for item, value in names.items():
        assert value == parse_docker_name(item)
