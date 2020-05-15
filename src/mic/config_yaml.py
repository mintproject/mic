from pathlib import Path

import click

CONFIG_YAML_NAME = "config.yaml"


def create_file_yaml(directory: Path, data_dir: Path, parameters: int) -> Path:
    config_yaml_path = directory / CONFIG_YAML_NAME
    try:
        with open(config_yaml_path, "w") as f:
            f.write("test")
    except Exception as e:
        click.secho("Failed: Error message {}".format(e), fg="red")
        exit(1)
    click.secho("Created: {}".format(config_yaml_path.absolute()), fg="green")
    return config_yaml_path
