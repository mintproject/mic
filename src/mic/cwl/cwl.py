from pathlib import Path
from typing import Dict

import click
import yaml

from mic.component.reprozip import format_code
from mic.config_yaml import write_to_yaml
from mic.constants import PARAMETERS_KEY, DEFAULT_DESCRIPTION_KEY, DEFAULT_VALUE_KEY, DATATYPE_KEY, NAME_KEY, PATH_KEY, \
    OUTPUTS_KEY, INPUTS_KEY

parameter_list = ["int", "boolean", "string"]
input_list = ["File"]


def is_parameters(_type: str):
    _exit = True if _type in parameter_list else False
    return _exit


def is_input(_type: str):
    _exit = True if _type in input_list else False
    return _exit


def get_parameters(spec: Dict):
    parameters = {}
    for key, item in spec["inputs"].items():
        if "type" in item and item["type"]:
            parameters[key] = item
    return parameters


def get_inputs(spec: Dict):
    parameters = []
    for key, item in spec["inputs"].items():
        if "type" in item and item["type"]:
            parameters.append(item)
    return parameters


def get_docker_image(cwl_spec):
    if "hints" in cwl_spec and "DockerRequirement" in cwl_spec['hints']:
        return cwl_spec['hints']['DockerRequirement']['dockerImageId']
    else:
        raise ValueError("Unable to find the Docker Image")


def get_base_command(cwl_spec):
    if "baseCommand" in cwl_spec:
        return cwl_spec['baseCommand']
    else:
        raise ValueError("Unable to find the Base Command")


def supported(cwl_spec):
    if "class" in cwl_spec and cwl_spec["class"] == "CommandLineTool":
        pass
    else:
        raise ValueError("Unsuported class")


def add_parameters(config_yaml_path: Path, cwl_spec: Dict, values: Dict):
    spec = yaml.load(config_yaml_path.open(), Loader=yaml.Loader)
    spec[PARAMETERS_KEY] = {}
    for key, item in cwl_spec.items():
        name = key
        value = values[key]
        type_value = type(value).__name__
        description = ""
        new_par = {name: {NAME_KEY: name,
                          DEFAULT_VALUE_KEY: value,
                          DATATYPE_KEY: type_value,
                          DEFAULT_DESCRIPTION_KEY: description}}

        spec[PARAMETERS_KEY].update(new_par)
    try:
        write_to_yaml(config_yaml_path, spec)
    except Exception as e:
        click.secho("Failed: Error message {}".format(e), fg="red")
    for item in spec[PARAMETERS_KEY]:
        click.secho("Added: {} as a parameter".format(item))


def add_inputs(config_yaml_path: Path, cwl_spec: Dict, valuies: Dict):
    spec = yaml.load(config_yaml_path.open(), Loader=yaml.Loader)
    spec[INPUTS_KEY] = {}
    write_to_yaml(config_yaml_path, spec)


def add_outputs(config_yaml_path: Path, cwl_spec: Dict, values: Dict):
    spec = yaml.load(config_yaml_path.open(), Loader=yaml.Loader)
    spec[OUTPUTS_KEY] = {}
    for key, item in cwl_spec.items():
        name = key
        value = values[key]
        description = ""
        new_par = {name: {NAME_KEY: name,
                          PATH_KEY: value,
                          DEFAULT_DESCRIPTION_KEY: description}}

        spec[OUTPUTS_KEY].update(new_par)
    try:
        write_to_yaml(config_yaml_path, spec)
    except Exception as e:
        click.secho("Failed: Error message {}".format(e), fg="red")
    for item in spec[OUTPUTS_KEY]:
        click.secho("Added: {} as a output".format(item))


def generate_runner(spec, user_execution_directory, mic_inputs, mic_outputs, mic_parameters):
    code = ''
    for key, item in parameters.items():
        cwl_line = f"{base_command} {item['inputBinding']['prefix']} {cwl_values[key]}"