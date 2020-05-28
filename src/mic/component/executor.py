import logging
import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

import click
import docker
from dame.executor import build_parameter, build_output
from mic.component.initialization import render_output
from mic.config_yaml import get_inputs_parameters, write_spec, add_outputs
from mic.constants import SRC_DIR, EXECUTIONS_DIR, DOCKER_DIR, DOCKER_KEY, LAST_EXECUTION_DIR
from mic.publisher.model_catalog import create_model_catalog_resource


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
            if is_directory:
                shutil.copytree(input_path, src_dir_path / input_path.name)
            else:
                shutil.copy(input_path, src_dir_path / input_path.name)
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


def clean_execution_directory(model_path: Path):
    execution_dir = model_path / EXECUTIONS_DIR
    shutil.rmtree(execution_dir)


def run_execution(line, execution_dir):
    proc = subprocess.Popen(line.split(' '), cwd=execution_dir)
    proc.wait()
    return proc.returncode


def execute(mint_config_file: Path):
    model_path = mint_config_file.parent
    execution_dir = create_execution_directory(mint_config_file, model_path)
    resource = create_model_catalog_resource(mint_config_file)
    try:
        line = get_command_line(resource)
    except:
        logging.error("Unable to cmd_line", exc_info=True)
    click.secho("Running\n{}".format(line))
    if run_execution(line, execution_dir) == 0:
        click.secho("Success", fg="green")
    else:
        click.secho("Failed", fg="red")


def build_docker(docker_path: Path, name: str):
    client = docker.from_env()
    image, logs = client.images.build(path=str(docker_path), tag="{}".format(name), nocache=True)
    for chunk in logs:
        print(chunk)
    return image.tags[0]
    # return docker_image_name


def execute_using_docker(mint_config_file: Path):
    model_path = mint_config_file.parent
    name = model_path.name
    docker_path = model_path / DOCKER_DIR
    image = build_docker(docker_path, name)
    now = datetime.now().timestamp()

    src_dir = create_execution_directory(mint_config_file, model_path)
    try:
        resource = create_model_catalog_resource(mint_config_file)
    except ValueError:
        pass

    docker_run(image, resource, src_dir)
    detect_news_file(src_dir, mint_config_file, now)
    write_spec(mint_config_file, LAST_EXECUTION_DIR, str(src_dir.absolute()))
    return src_dir


def docker_run(image, resource, src_dir):
    mint_volumes = {str(src_dir.absolute()): {'bind': '/tmp/mint', 'mode': 'rw'}}
    try:
        line = get_command_line(resource)
    except:
        logging.error("Unable to cmd_line", exc_info=True)
    click.secho("Running \n {}".format(line), fg="green")
    try:
        client = docker.from_env()
        res = client.containers.run(command=line,
                                    image=image,
                                    volumes=mint_volumes,
                                    working_dir='/tmp/mint',
                                    detach=True,
                                    stream=True,
                                    remove=True
                                    )
        for chunk in res.logs(stream=True):
            print(chunk)
        click.secho("Success", fg="green")

    except Exception as e:
        click.secho("Failed", fg="red")
        logging.error(e, exc_info=True)


def compress_file(detected_files):
    return click.confirm("Do you want to create one zip files with the files?", default=False)


def detect_news_file(src_directory: Path, mint_config_file: Path, time: datetime):
    """
    Get the files by a modification timestamp.
    :param src_directory: The src execution dir
    :type src_directory: Path
    :param mint_config_file: The mic configuration file
    :type mint_config_file: Path
    :param time: Execution time
    :type time: datetime
    """
    model_name = mint_config_file.parent.name
    files_list = []
    for root, _, filenames in os.walk(src_directory, topdown=True):
        for filename in filenames:
            filepath = os.path.join(os.path.abspath(root), filename)
            created = os.path.getmtime(Path(filepath))
            modified = os.path.getmtime(Path(filepath))
            if time < created or time < modified:
                files_list.append(Path(filepath).relative_to(src_directory))
    if files_list:
        model_dir = mint_config_file.parent
        click.secho("The model has generated the following files")
        for file in files_list:
            print(file)
        render_output(model_dir, files_list, None)
        add_outputs(mint_config_file, files_list)


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
