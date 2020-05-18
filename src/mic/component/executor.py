import os
import shutil
from pathlib import Path

import click
from jinja2 import Environment, select_autoescape, FileSystemLoader
from mic.config_yaml import get_configuration_files, get_inputs_parameters
from mic.constants import SRC_DIR, EXECUTIONS_DIR


def copy_file(input_path: Path, src_dir_path: Path):
    return shutil.copyfile(input_path, src_dir_path / input_path.name)


def compress_directory(mint_config_file: Path):
    pass


def _copy_directory(src: Path, dest: Path) -> Path:
    pass


def copy_inputs(mint_config_file: Path, src_dir_path: Path):
    model_path = mint_config_file.parent
    inputs, parameters, _ = get_inputs_parameters(mint_config_file)
    for _, item in inputs.items():
        input_path = model_path / item['path']
        is_directory = True if input_path.resolve.is_dir() else False
        try:
            os.symlink(input_path, src_dir_path / input_path.name, target_is_directory=is_directory)
            src_file = copy_file(input_path, src_dir_path)
            click.secho("Added: {}".format(src_file), fg="green")
        except OSError as e:
            click.secho("Failed: Error message "
                        "On newer versions of Windows 10, unprivileged accounts can create"
                        " symlinks if Developer Mode is enabled. When Developer Mode is not"
                        " available/enabled, the SeCreateSymbolicLinkPrivilege privilege is required, "
                        "or the process must be run as an administrator."
                        "{}".format(e), fg="red")

        except Exception as e:
            click.secho("Failed: Error message {}".format(e), fg="red")


def create_execution_directory(mint_config_file: Path, model_path: Path):
    from datetime import datetime
    execution_name = datetime.now().strftime("%m_%d_%H_%M_%S")
    execution_dir = model_path / EXECUTIONS_DIR / execution_name
    execution_dir.mkdir(parents=True)
    _copy_directory(model_path / SRC_DIR, execution_dir / SRC_DIR)
    copy_inputs(mint_config_file, execution_dir / SRC_DIR)


def run_execution():
    pass


def execute(mint_config_file: Path):
    model_path = mint_config_file.parent
    create_execution_directory(mint_config_file, model_path)
    run_execution()


def replace_parameters(mint_config_file: Path, src_directory=Path('.')):
    """
    You must run this method in the src directory
    """
    env = Environment(
        loader=FileSystemLoader(src_directory),
        autoescape=select_autoescape(['html', 'xml']),
        trim_blocks=False,
        lstrip_blocks=False
    )
    _, parameters, _ = get_inputs_parameters(mint_config_file)
    configuration_files = [Path(file_path) for file_path in get_configuration_files(mint_config_file)]
    for item in configuration_files:
        template = env.get_template(item.name)
        with open(item, "w") as f:
            f.write(template.render(template=template, **parameters))
