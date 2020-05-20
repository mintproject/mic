import logging
import os
import shutil
import subprocess
import uuid
from pathlib import Path

import click
from dame.cli_methods import create_sample_resource
from dame.executor import build_parameter, build_output
from mic.config_yaml import get_inputs_parameters
from mic.constants import SRC_DIR, EXECUTIONS_DIR, DATA_DIR
from modelcatalog import ModelConfiguration, DatasetSpecification, Parameter


def generate_uuid():
    return "https://w3id.org/okn/i/mint/{}".format(str(uuid.uuid4()))


def copy_file(input_path: Path, src_dir_path: Path):
    return shutil.copyfile(input_path, src_dir_path / input_path.name)


def compress_directory(mint_config_file: Path):
    pass


def _copy_directory(src: Path, dest: Path) -> Path:
    return shutil.copytree(src, dest)


def copy_inputs(mint_config_file: Path, src_dir_path: Path):
    model_path = mint_config_file.parent
    inputs, parameters, _, _ = get_inputs_parameters(mint_config_file)
    for _, item in inputs.items():
        input_path = model_path / item['path']
        is_directory = True if input_path.is_dir() else False
        try:
            os.symlink(input_path, src_dir_path / input_path.name, target_is_directory=is_directory)
            click.secho("Added: {} into the execution directory".format(input_path.name), fg="green")
        except OSError as e:
            click.secho("Failed: Error message {}".format(e), fg="red")

        except Exception as e:
            click.secho("Failed: Error message {}".format(e), fg="red")
    click.secho("The execution directory is available {}".format(src_dir_path), fg="green")


def create_execution_directory(mint_config_file: Path, model_path: Path):
    from datetime import datetime
    execution_name = datetime.now().strftime("%m_%d_%H_%M_%S")
    execution_dir = model_path / EXECUTIONS_DIR / execution_name
    execution_dir.mkdir(parents=True)
    src_executions_dir = execution_dir / SRC_DIR
    _copy_directory(model_path / SRC_DIR, src_executions_dir)
    copy_inputs(mint_config_file, src_executions_dir)
    return src_executions_dir


def create_model_catalog_resource(mint_config_file):
    name = mint_config_file.parent
    inputs, parameters, outputs, _ = get_inputs_parameters(mint_config_file)
    model_catalog_inputs = []
    model_catalog_parameters = []
    model_catalog_outputs = []

    position = 1

    for key, item in inputs.items():
        try:
            if Path(item["path"]).is_dir():
                _format = "zip"
            else:
                _format = item["path"].name.split('.')[-1]
        except:
            _format = "unknown"
        _input = DatasetSpecification(id=generate_uuid(), label=key, has_format=format, position=[position])
        create_sample_resource(_input, str(Path(name / item["path"]).resolve()))
        model_catalog_inputs.append(_input)
        position += 1

    position = 1
    for key, item in parameters.items():
        _parameter = Parameter(id=generate_uuid(), label=key, position=[position])
        _parameter.has_default_value = [item["default_value"]]
        model_catalog_parameters.append(_parameter)
        position += 1

    return ModelConfiguration(id=generate_uuid(),
                              label=name,
                              has_input=model_catalog_inputs,
                              has_output=model_catalog_outputs,
                              has_parameter=model_catalog_parameters)


def run_execution(line, execution_dir):
    proc = subprocess.Popen(line.split(' '), cwd=execution_dir)
    proc.wait()


def execute(mint_config_file: Path):
    model_path = mint_config_file.parent
    execution_dir = create_execution_directory(mint_config_file, model_path)
    resource = create_model_catalog_resource(mint_config_file)
    try:
        line = get_command_line(resource)
    except:
        logging.error("Unable to cmd_line", exc_info=True)
    click.secho("Running \n {}".format(line), fg="green")
    run_execution(line, execution_dir)


def get_command_line(resource):
    line = './run '
    inputs = resource.has_input
    try:
        parameters = resource.has_parameter
    except:
        parameters = None
    outputs = resource.has_output
    if inputs:
        l = build_input(inputs)
        line += " {}".format(l)
    if outputs:
        l = build_output(outputs)
        line += " {}".format(l)
    if parameters is not None:
        l = build_parameter(parameters)
        line += " {}".format(l)
    return line


def build_input(inputs):
    """
    Download or search the file. Loop the inputs (metadata) of Model Configuration or Model Configuration Setup
    """
    line = ""
    for _input in inputs:
        _file_path = _input.has_fixed_resource[0]["value"][0]
        _format = _input.format[0] if hasattr(_input, "format") else None
        file_name = _file_path
        position = _input.position[0]
        line += " -i{} {}".format(position, file_name)
    return line
