import logging
import shutil
import subprocess
from pathlib import Path

import click
from dame.executor import build_parameter, build_output
from mic.config_yaml import get_key_spec, get_inputs
from mic.constants import SRC_DIR, EXECUTIONS_DIR, PATH_KEY, DATA_DIR, INPUTS_KEY
from mic.publisher.model_catalog import create_model_catalog_resource


def copy_file(input_path: Path, src_dir_path: Path):
    return shutil.copyfile(input_path, src_dir_path / input_path.name)


def compress_directory(directory_path: Path, working_dir):
    zip_file_path = shutil.make_archive(directory_path.name, 'zip', root_dir=directory_path.parent,
                                        base_dir=directory_path.name)
    data_zip = working_dir / Path(zip_file_path).name
    shutil.move(zip_file_path, data_zip)
    return data_zip


def _copy_directory(src: Path, dest: Path) -> Path:
    return shutil.copytree(src, dest)


def create_execution_directory(mic_config_file: Path, execution_name):
    model_path = mic_config_file.parent
    execution_dir = model_path / EXECUTIONS_DIR / execution_name
    execution_dir.mkdir(parents=True)
    click.secho("Create a execution directory {}".format(execution_dir))
    src_executions_dir = execution_dir / SRC_DIR
    _copy_directory(model_path / SRC_DIR, src_executions_dir)
    click.secho(f"""Copying the inputs
Source: {model_path / DATA_DIR}
Destination: {src_executions_dir}""")
    spec = get_inputs(mic_config_file)
    for key, value in spec.items():
        file = model_path / DATA_DIR / str(Path(value[PATH_KEY]).name)
        copy_file(file, src_executions_dir)

    return src_executions_dir


def run_execution(line, execution_dir):
    proc = subprocess.Popen(line.split(' '), cwd=execution_dir)
    proc.wait()
    return proc.returncode


def execute_local(mint_config_file: Path, execution_name):
    execution_dir = create_execution_directory(mint_config_file, execution_name)
    resource = create_model_catalog_resource(mint_config_file, name=None, execution_dir=execution_dir)
    try:
        line = get_command_line(resource)
    except:
        logging.error("Unable to cmd_line", exc_info=True)
    click.secho("Running\n{}".format(line))
    if run_execution(line, execution_dir) == 0:
        return True
    else:
        return False


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


def copy_code_to_src(code_files, user_execution_directory, src_dir):
    for key, item in code_files.items():
        file_path = user_execution_directory / item[PATH_KEY]
        relative_to = src_dir.relative_to(user_execution_directory)
        click.secho(f"""Copying the code: {file_path.name} to the MIC Wrapper directory {relative_to}""")
        shutil.copyfile(file_path, src_dir / file_path.name)


def copy_config_to_src(code_files, user_execution_directory, src_dir):
    for key, item in code_files.items():
        file_path = user_execution_directory / item[PATH_KEY]
        relative_to = src_dir.relative_to(user_execution_directory)
        click.secho(f"""Copying the config: {file_path.name} to the MIC Wrapper directory {relative_to}""")
        shutil.copyfile(file_path, src_dir / file_path.name)
