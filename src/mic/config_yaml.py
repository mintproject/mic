import logging
import random
import re
import unicodedata
from pathlib import Path

import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

import click
from mic._makeyaml import make_yaml
from mic.constants import *


def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower()).strip()
    return re.sub(r'[-\s]+', '-', value)


def random_parameter():
    return random.choice(["a random string", True, 1.0, 1])


def create_file_yaml(directory: Path, data_dir: Path, parameters: int) -> Path:
    config_yaml_path = directory / CONFIG_YAML_NAME
    if data_dir.exists():
        click.secho("Searching files in the directory {}".format(data_dir))
    else:
        click.secho("Failed: Directory {} doesn't exist".format(data_dir), fg="red")
        exit(1)
    try:
        spec = {}
        input_files = [x for x in data_dir.iterdir()]
        if input_files:
            spec[INPUTS_KEY] = {}
        if parameters:
            spec[PARAMETERS_KEY] = {}

        for index, item in enumerate(input_files):
            name = slugify(str(item.name).split('.')[0])
            spec[INPUTS_KEY][name] = {}
            spec[INPUTS_KEY][name][PATH_KEY] = str(item.relative_to(directory))
    except Exception as e:
        logging.error(e, exc_info=True)
        click.secho("Failed: Error message {}".format(e), fg="red")
        exit(1)

    try:
        for parameter in range(0, parameters):
            name = "parameter{}".format(parameter + 1)
            spec[PARAMETERS_KEY][name] = {}
            spec[PARAMETERS_KEY][name][DEFAULT_VALUE_KEY] = random_parameter()

        with open(config_yaml_path, 'w') as f:
            yaml.dump(spec, f, sort_keys=False)

    except Exception as e:
        logging.error(e, exc_info=True)
        click.secho("Failed: Error message {}".format(e), fg="red")
        exit(1)
    click.secho("Created: {}".format(config_yaml_path.absolute()), fg="green")
    return config_yaml_path


def add_configuration_files(config_yaml_path: Path, configurations: tuple):
    spec = yaml.load(config_yaml_path.open(), Loader=Loader)
    spec["config_file"] = [str(Path(x).relative_to(config_yaml_path.parent))  for x in list(configurations)]
    with open(config_yaml_path, 'w') as f:
        yaml.dump(spec, f, sort_keys=False)

def get_inputs_parameters(config_yaml_path: Path) -> (dict, dict, dict):
    spec = yaml.load(config_yaml_path.open(), Loader=Loader)
    inputs = spec[INPUTS_KEY] if INPUTS_KEY in spec else None
    parameters = spec[PARAMETERS_KEY] if PARAMETERS_KEY in spec else None
    outputs = spec[OUTPUTS_KEY] if OUTPUTS_KEY in spec else None
    return inputs, parameters, outputs


def get_numbers_inputs_parameters(config_yaml_path: Path) -> (int, int, int):
    spec = yaml.load(config_yaml_path.open(), Loader=Loader)
    number_inputs = len(spec[INPUTS_KEY].keys()) if INPUTS_KEY in spec else 0
    number_parameters = len(spec[PARAMETERS_KEY].keys()) if PARAMETERS_KEY in spec else 0
    number_outputs = len(spec[OUTPUTS_KEY].keys()) if OUTPUTS_KEY in spec else 0
    return number_inputs, number_parameters, number_outputs


def create_file_yaml_basic(config_yaml_path: Path):
    make_yaml(config_yaml_path)
