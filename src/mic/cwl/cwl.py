from datetime import datetime
from pathlib import Path
from typing import Dict

import click
import yaml
import logging
from mic._utils import check_mic_path
from mic.cli_docs import info_start_run, info_end_run, info_end_run_failed
from mic.component.executor import execute_local
from mic.component.reprozip import format_code
from mic.config_yaml import write_to_yaml
from mic.constants import PARAMETERS_KEY, DEFAULT_DESCRIPTION_KEY, DEFAULT_VALUE_KEY, DATATYPE_KEY, NAME_KEY, PATH_KEY, \
    OUTPUTS_KEY, INPUTS_KEY, EXECUTIONS_DIR

parameter_list = ["int", "boolean", "string"]
file_list = ["File"]


def is_parameter(_type: str):
    _exit = True if _type in parameter_list else False
    return _exit


def is_input(_type: str):
    _exit = True if _type in file_list else False
    return _exit


def get_parameters(spec: Dict):
    parameters = {}
    for key, item in spec["inputs"].items():
        if "type" in item and is_parameter(item["type"]):
            parameters[key] = item
    return parameters


def get_inputs(spec: Dict):
    inputs = {}
    for key, item in spec["inputs"].items():
        if "type" in item and is_input(item["type"]):
            inputs[key] = item
    return inputs


def get_outputs(spec: Dict):
    files = {}
    for key, item in spec["outputs"].items():
        if "type" in item and is_input(item["type"]):
            files[key] = item
    return files

def get_docker_image(cwl_spec: Dict):
    if "hints" in cwl_spec and "DockerRequirement" in cwl_spec['hints']:
        return cwl_spec['hints']['DockerRequirement']['dockerImageId']
    else:
        raise ValueError("Unable to find the Docker Image")

def update_docker_image(cwl_spec_path: Path, docker_image: str):
    cwl_spec = yaml.load(cwl_spec_path.open(), Loader=yaml.Loader)
    if "hints" in cwl_spec and "DockerRequirement" in cwl_spec['hints']:
        cwl_spec['hints']['DockerRequirement']['dockerImageId'] = docker_image
    else:
        raise ValueError("Unable to find the Docker Image")
    try:
        write_to_yaml(cwl_spec_path, cwl_spec)
    except Exception as e:
        click.secho("Failed: Error message {}".format(e), fg="red")
    click.secho("Docker Image has been updated  {} in the CWL specification".format(docker_image))


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


def add_inputs(config_yaml_path: Path, cwl_spec: Dict, values: Dict):
    spec = yaml.load(config_yaml_path.open(), Loader=yaml.Loader)
    spec[INPUTS_KEY] = {}
    for key, item in cwl_spec.items():
        name = key
        value = values[key] if key in values else ""
        description = ""
        new_par = {name: {NAME_KEY: name,
                          DEFAULT_DESCRIPTION_KEY: description}}

        spec[INPUTS_KEY].update(new_par)
    try:
        write_to_yaml(config_yaml_path, spec)
    except Exception as e:
        click.secho("Failed: Error message {}".format(e), fg="red")
    for item in spec[INPUTS_KEY]:
        click.secho("Added: {} as a input".format(item))


def add_outputs(config_yaml_path: Path, cwl_spec: Dict, values: Dict):
    spec = yaml.load(config_yaml_path.open(), Loader=yaml.Loader)
    spec[OUTPUTS_KEY] = {}
    for key, item in cwl_spec.items():
        name = key
        value = values[key] if key in values else ""
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
