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
input_list = ["File"]


def is_parameter(_type: str):
    _exit = True if _type in parameter_list else False
    return _exit


def is_input(_type: str):
    _exit = True if _type in input_list else False
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


def get_docker_image(cwl_spec):
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
        click.secho("Added: {} as a output".format(item))


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

def run(mic_file):
    """
  This step will test the model component you created in previous steps.

  - You must pass the MIC_FILE (mic.yaml) using the option (-f) or run the
  command from the same directory as mic.yaml

  mic pkg run -f <mic_file>

  Example:

  mic pkg wrapper -f mic/mic.yaml
    """
    # Searches for mic file if user does not provide one
    mic_file = check_mic_path(mic_file)

    try:
        execution_name = datetime.now().strftime("%m_%d_%H_%M_%S")
        mic_config_path = Path(mic_file)
        execution_dir = Path(mic_config_path.parent / EXECUTIONS_DIR / execution_name)
        info_start_run(execution_dir.relative_to(mic_config_path.parent.parent))
        if execute_local(mic_config_path, execution_name):
            info_end_run(execution_dir)
            logging.info("Run passed")
            click.echo("You model has passed all the tests. Please, review the outputs files.")
            click.echo('If the model is ok, type "exit" to go back to your computer')
            click.echo('IMPORTANT: type "exit" and then upload your Model Component')
        else:
            logging.warning("Run failed")
            info_end_run_failed()

        logging.info("run done")
    except Exception as e:
        logging.exception(f"Run failed: {e}")
        click.secho("Failed", fg="red")

