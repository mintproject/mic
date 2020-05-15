import copy
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
from mic import _schema
from mic._makeyaml import make_yaml, write_properties
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
        schema = write_properties(_schema.get_schema()["properties"])
        input_files = [x for x in data_dir.iterdir()]

        if input_files:
            spec[INPUTS_KEY] = schema[INPUTS_KEY].copy()
        if parameters:
            spec[PARAMETERS_KEY] = schema[PARAMETERS_KEY].copy()

        for index, item in enumerate(input_files):
            temp = copy.deepcopy(schema[INPUTS_KEY])[0]
            if index >= len(spec[INPUTS_KEY]):
                spec[INPUTS_KEY].append(temp)
            else:
                spec[INPUTS_KEY][index] = temp
            spec[INPUTS_KEY][index][NAME_KEY] = slugify(str(item.name).split('.')[0])
            spec[INPUTS_KEY][index][PATH_KEY] = str(item.relative_to(directory))
    except Exception as e:
        logging.error(e, exc_info=True)
        click.secho("Failed: Error message {}".format(e), fg="red")
        exit(1)

    try:
        for parameter in range(0, parameters):
            temp = copy.deepcopy(schema[PARAMETERS_KEY])[0]
            if parameter >= len(spec[PARAMETERS_KEY]):
                spec[PARAMETERS_KEY].append(temp)
            else:
                spec[PARAMETERS_KEY][parameter] = temp
            spec[PARAMETERS_KEY][parameter][NAME_KEY] = "parameter{}".format(parameter + 1)
            spec[PARAMETERS_KEY][parameter][DEFAULT_VALUE_KEY] = random_parameter()

        with open(config_yaml_path, 'w') as f:
            yaml.dump(spec, f, sort_keys=False)

    except Exception as e:
        logging.error(e, exc_info=True)
        click.secho("Failed: Error message {}".format(e), fg="red")
        exit(1)
    click.secho("Created: {}".format(config_yaml_path.absolute()), fg="green")
    return config_yaml_path


def get_inputs_parameters(config_yaml_path: Path) -> (dict,dict, dict):
    spec = yaml.load(config_yaml_path.open(), Loader=Loader)
    inputs = spec[INPUTS_KEY] if INPUTS_KEY in spec else None
    parameters = spec[PARAMETERS_KEY] if PARAMETERS_KEY in spec else None
    outputs = spec[OUTPUTS_KEY] if OUTPUTS_KEY in spec else None
    return inputs, parameters, outputs


def get_numbers_inputs_parameters(config_yaml_path: Path) -> (int, int, int):
    spec = yaml.load(config_yaml_path.open(), Loader=Loader)
    number_inputs = len(spec[INPUTS_KEY]) if INPUTS_KEY in spec else 0
    number_parameters = len(spec[PARAMETERS_KEY]) if PARAMETERS_KEY in spec else 0
    number_outputs = len(spec[OUTPUTS_KEY]) if OUTPUTS_KEY in spec else 0
    return number_inputs, number_parameters, number_outputs


def create_file_yaml_basic(config_yaml_path: Path):
    make_yaml(config_yaml_path)
