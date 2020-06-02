import logging
import random
import re
import unicodedata
from pathlib import Path
from typing import List

import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

import click
from mic._makeyaml import make_yaml
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
    return 0


def create_config_file_yaml(model_path: Path) -> Path:
    config_yaml_path = model_path / CONFIG_YAML_NAME
    if model_path.exists():
        click.secho("Searching files in the directory {}".format(model_path))
    else:
        click.secho("Failed: Directory {} doesn't exist".format(model_path), fg="red")
        exit(1)
    spec = {}
    write_step(config_yaml_path, spec, step=1)


def get_spec(config_yaml_path: Path) -> dict:
    spec = yaml.load(config_yaml_path.open(), Loader=Loader)
    return spec


def get_key_spec(config_yaml_path: Path, key: str):
    spec = yaml.load(config_yaml_path.open(), Loader=Loader)
    if key in spec:
        return spec[key]
    return None


def write_spec(config_yaml_path: Path, key: str, value: object):
    spec = yaml.load(config_yaml_path.open(), Loader=Loader)
    spec[key] = value
    write_to_yaml(config_yaml_path, spec)


def get_key_spec(config_yaml_path: Path, key: str):
    spec = yaml.load(config_yaml_path.open(), Loader=Loader)
    if key in spec:
        return spec[key]
    return None


def write_spec(config_yaml_path: Path, key: str, value: object):
    spec = yaml.load(config_yaml_path.open(), Loader=Loader)
    spec[key] = value
    write_to_yaml(config_yaml_path, spec)


def write_step(config_yaml_path: Path, spec: dict, step: int):
    spec[STEP_KEY] = step
    write_to_yaml(config_yaml_path, spec)


def write_docker_image(config_yaml_path: Path, spec: dict, image_name: str):
    spec[DOCKER_KEY] = {NAME_KEY : image_name}
    write_to_yaml(config_yaml_path, spec)


def write_docker_image(config_yaml_path: Path, spec: dict, image_name: str):
    spec[DOCKER_KEY] = {NAME_KEY: image_name}
    write_to_yaml(config_yaml_path, spec)


def fill_config_file_yaml(config_yaml_path: Path, data_dir: Path, parameters: int) -> Path:
    directory = config_yaml_path.parent
    if data_dir.exists():
        click.secho("Searching files in the directory {}".format(data_dir))
    else:
        click.secho("Failed: Directory {} doesn't exist".format(data_dir), fg="red")
        exit(1)
    try:
        spec = {}
        input_files = []
        for x in data_dir.iterdir():
            if not x.name.startswith('.'):
                input_files.append(x)
        if input_files:
            spec[INPUTS_KEY] = {}

        if parameters:
            spec[PARAMETERS_KEY] = {}

        for index, item in enumerate(input_files):
            name = slugify(str(item.name).replace('.', "_"))
            spec[INPUTS_KEY][name] = {}
            spec[INPUTS_KEY][name][PATH_KEY] = str(item.relative_to(directory))
            spec[INPUTS_KEY][name][DEFAULT_DESCRIPTION_KEY] = ""

    except Exception as e:
        logging.error(e, exc_info=True)
        click.secho("Failed: Error message {}".format(e), fg="red")
        exit(1)

    try:
        for parameter in range(0, parameters):
            name = "parameter{}".format(parameter + 1)
            spec[PARAMETERS_KEY][name] = {}
            spec[PARAMETERS_KEY][name][DEFAULT_VALUE_KEY] = random_parameter()
            spec[PARAMETERS_KEY][name][DEFAULT_DESCRIPTION_KEY] = ""

        write_step(config_yaml_path, spec, step=2)
        add_comment(config_yaml_path, DEFAULT_VALUE_KEY, DEFAULT_PARAMETER_COMMENT)
        add_comment(config_yaml_path, DEFAULT_DESCRIPTION_KEY, DEFAULT_DESCRIPTION_MESSAGE)
    except Exception as e:
        logging.error(e, exc_info=True)
        click.secho("Failed: Error message {}".format(e), fg="red")
        exit(1)
    click.secho("MIC has added the parameters and inputs into the {}".format(MIC_CONFIG_FILE_NAME), fg="green")
    click.secho("You can see the changes {}".format(config_yaml_path.absolute()), fg="green")
    return config_yaml_path


def write_to_yaml(config_yaml_path: Path, spec):
    """
    This function makes sure that the comments get saved when writing new data to the yaml file
    @param config_yaml_path: path
    @param spec: data for yaml
    """
    comments = []
    if config_yaml_path.exists():
        comments = get_comment_list(config_yaml_path)

    with open(config_yaml_path, 'w') as f:
        yaml.dump(spec, f, sort_keys=False)

    # yaml.dump will override comments in original yaml file. this will replace them
    for i in comments:
        new_line = False
        if i['value'] is None or i['value'] == "":
            new_line = True

        add_comment_by_line(config_yaml_path, i['line_number'], new_line, i['comment'])


def get_comment_list(config_yaml_path: Path):
    """
    Return list of all the yaml values that have comments. This is needed becasue yaml.dump will erase any comments in
    the yaml
    @param config_yaml_path: path to yaml
    @type config_yaml_path: Path
    @return: list
    """
    all_comments = []
    count = 0
    with open(config_yaml_path, "r") as file:
        for line in file:
            count += 1
            value_comment_line = {'value': "", 'line_number': count, 'comment': ""}
            if "#" in line:
                for i in line.split(" "):
                    if ":" in i:
                        value_comment_line['value'] = i

                curr_comment = line.split("#")
                curr_comment.pop(0)
                curr_comment = "#" + "#".join(curr_comment).replace("\n", "")
                value_comment_line['comment'] = curr_comment
                value_comment_line['line_number'] = count
                if value_comment_line not in all_comments:
                    # deep copy
                    all_comments.append({'value': value_comment_line['value'],
                                         'line_number': value_comment_line['line_number'],
                                         'comment': value_comment_line['comment']})

    return all_comments


def add_comment_by_line(config_yaml_path: Path, line_number, insert_new_line, comment):
    """
    Adds comment to yaml file from line number

    @param config_yaml_path: path
    @param line_number: line number comment is on
    @param insert_new_line: If the comment was on a line without a value. Added comment needs to insert on new line
    @param comment: comment to append
    @return:
    """
    new_file = []
    count = 0
    with open(config_yaml_path, "r") as file:
        for line in file:
            count += 1
            if line_number == count:
                # make sure comment character is in comment
                if "#" not in comment:
                    comment = "# " + comment
                if not insert_new_line:
                    new_file.append(line.replace("\n", "  " + comment + "\n"))
                else:
                    new_file.append(comment + "\n")
                    new_file.append(line)
            else:
                new_file.append(line)

        if line_number > count:
            new_file.append(comment + "\n")

    with open(config_yaml_path, "w") as file:
        file.writelines(new_file)


def add_comment(config_yaml_path: Path, value, comment):
    """
    yaml does not natively support comments, so this workaround has to be implemented. This function reads through
    the yaml file and looks for the value given, then appends a comment to the end
    @param config_yaml_path:
    @type config_yaml_path: Path
    @param value: name of field to append comment to
    @type value: str
    @param comment: comment to append
    @type comment: str
    """
    new_file = []
    with open(config_yaml_path, "r") as file:
        for line in file:
            # if the value is in line and line doesnt have comment
            if value in line and "#" not in line:
                # make sure comment character is in comment
                if "#" not in comment:
                    comment = "# " + comment

                new_file.append(line.replace("\n", "  " + comment + "\n"))
            else:
                new_file.append(line)

    with open(config_yaml_path, "w") as file:
        file.writelines(new_file)


def add_outputs(config_yaml_path: Path, outputs: List[Path]):
    spec = yaml.load(config_yaml_path.open(), Loader=Loader)
    spec[OUTPUTS_KEY] = {}
    for x in outputs:
        name = slugify(str(x).replace('.', "_"))
        spec[OUTPUTS_KEY][name] = {'path':  str(x)}
        spec[OUTPUTS_KEY][name][DEFAULT_DESCRIPTION_KEY] = ""
    try:
        write_to_yaml(config_yaml_path, spec)
        add_comment(config_yaml_path, DEFAULT_DESCRIPTION_KEY, DEFAULT_DESCRIPTION_MESSAGE)
    except Exception as e:
        click.secho("Failed: Error message {}".format(e), fg="red")
    for item in spec[OUTPUTS_KEY]:
        click.secho("Added: {} as a output".format(item), fg="green")


def add_configuration_files(config_yaml_path: Path, configurations: tuple):
    spec = yaml.load(config_yaml_path.open(), Loader=Loader)
    spec[CONFIG_FILE_KEY] = [str(Path(x).relative_to(config_yaml_path.parent)) for x in list(configurations)]

    try:
        write_to_yaml(config_yaml_path, spec)
    except Exception as e:
        click.secho("Failed: Error message {}".format(e), fg="red")
    for item in spec[CONFIG_FILE_KEY]:
        click.secho("Added: {} as a configuration file".format(item), fg="green")


def get_configuration_files(config_yaml_path: Path):
    spec = yaml.load(config_yaml_path.open(), Loader=Loader)
    return spec[CONFIG_FILE_KEY]


def get_inputs_parameters(config_yaml_path: Path) -> (dict, dict, dict):
    spec = yaml.load(config_yaml_path.open(), Loader=Loader)
    inputs = spec[INPUTS_KEY] if INPUTS_KEY in spec else None
    parameters = spec[PARAMETERS_KEY] if PARAMETERS_KEY in spec else None
    outputs = spec[OUTPUTS_KEY] if OUTPUTS_KEY in spec else None
    configs = spec[CONFIG_FILE_KEY] if CONFIG_FILE_KEY in spec else []
    return inputs, parameters, outputs, configs


def get_numbers_inputs_parameters(config_yaml_path: Path) -> (int, int, int):
    spec = yaml.load(config_yaml_path.open(), Loader=Loader)
    number_inputs = len(spec[INPUTS_KEY].keys()) if INPUTS_KEY in spec else 0
    number_parameters = len(spec[PARAMETERS_KEY].keys()) if PARAMETERS_KEY in spec else 0
    number_outputs = len(spec[OUTPUTS_KEY].keys()) if OUTPUTS_KEY in spec else 0
    return number_inputs, number_parameters, number_outputs


def create_file_yaml_basic(config_yaml_path: Path):
    make_yaml(config_yaml_path)
