from pathlib import Path

CONFIG_YAML_NAME = "config.yaml"


def create_file(directory: Path, data_dir: Path, parameters: int) -> Path:
    config_yaml_path = directory / CONFIG_YAML_NAME
    with open(config_yaml_path, "w") as f:
        f.write("test")
    return config_yaml_path
