import re
import unicodedata
from pathlib import Path
from typing import List

import click
import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

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


def create_config_file_yaml(model_path: Path) -> Path:
    config_yaml_path = model_path / CONFIG_YAML_NAME
    if not model_path.exists():
        click.secho("Failed: Directory {} doesn't exist".format(model_path), fg="red")
        exit(1)
    click.secho(f"{config_yaml_path} created", fg="green")
    if config_yaml_path.exists():
        spec = get_spec(config_yaml_path)
    else:
        spec = {}
    write_step(config_yaml_path, spec, step=1)
    return config_yaml_path


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


def write_step(config_yaml_path: Path, spec: dict, step: int):
    spec[STEP_KEY] = step
    write_to_yaml(config_yaml_path, spec)


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

                new_file.append(comment + "\n")
                new_file.append(line)
            else:
                new_file.append(line)

    with open(config_yaml_path, "w") as file:
        file.writelines(new_file)


def add_outputs(config_yaml_path: Path, outputs: List[Path]):
    spec = yaml.load(config_yaml_path.open(), Loader=Loader)
    spec[OUTPUTS_KEY] = {}
    for x in outputs:
        name = slugify(str(x).replace('.', "_"))
        spec[OUTPUTS_KEY][name] = {'path': str(x)}
        spec[OUTPUTS_KEY][name][DEFAULT_DESCRIPTION_KEY] = ""
    try:
        write_to_yaml(config_yaml_path, spec)
        add_comment(config_yaml_path, DEFAULT_DESCRIPTION_KEY, DEFAULT_DESCRIPTION_MESSAGE)
    except Exception as e:
        click.secho("Failed: Error message {}".format(e), fg="red")
    for item in spec[OUTPUTS_KEY]:
        click.secho("Added: {} as a output".format(item))

def add_params_from_config(yaml_path: Path, config_path: Path):
    """
    Add parameters to the mic.yaml file from the user's config file. Looks for ${var_name} in config file and
    adds the var_name as parameter to yaml

    @param yaml_path: path to mic.yaml file
    @type yaml_path: Path
    @param config_path: path to user's config file
    @type config_path: Path
    """
    mic_yaml = yaml.load(yaml_path.open(), Loader=Loader)
    var_list = []
    with open(config_path, "r") as f:
        file = f.readlines()
        for line in file:

            if "${" in line and "}" in line:
                tmp = line[line.find("${")+2:line.find("}")]
                var_list.append(tmp)

    # Add the var names as parameters
    added = False
    write_comment = True
    for name in var_list:

        if PARAMETERS_KEY not in mic_yaml:
            mic_yaml[PARAMETERS_KEY] = {}

        not_input = False
        not_output = False
        not_config = False

        if name not in mic_yaml[PARAMETERS_KEY]:
            if INPUTS_KEY not in mic_yaml:
                not_input = True
            elif name not in mic_yaml[INPUTS_KEY]:
                not_input = True
            if OUTPUTS_KEY not in mic_yaml:
                not_output = True
            elif name not in mic_yaml[OUTPUTS_KEY]:
                not_output = True
            if CONFIG_FILE_KEY not in mic_yaml:
                not_config = True
            elif name not in mic_yaml[CONFIG_FILE_KEY]:
                not_config = True

            if not_input and not_output and not_config:
                mic_yaml[PARAMETERS_KEY].update({name: {DEFAULT_VALUE_KEY: 0, DEFAULT_DESCRIPTION_KEY: "",
                                                        DATATYPE_KEY: ""}})
                click.secho("Automatically adding \"{}\" as a parameter".format(name))
                added = True

        write_spec(Path(yaml_path), PARAMETERS_KEY, mic_yaml[PARAMETERS_KEY])
        if write_comment and added:
            add_comment(yaml_path, PARAMETERS_KEY, "Add a default value and type to any automatically generated "
                                                   "parameters")
            add_comment(yaml_path, PARAMETERS_KEY, "It is also recommended you add a descriptions to your parameters")
            write_comment = False

    if added:
        click.secho("Default values will need to be added in {} for each parameter".format(CONFIG_YAML_NAME),fg="green")

def get_inputs_parameters(config_yaml_path: Path) -> (dict, dict, dict):
    inputs = get_inputs(config_yaml_path)
    parameters = get_parameters(config_yaml_path)
    outputs = get_outputs_mic(config_yaml_path)
    configs = get_configs(config_yaml_path)
    return inputs, parameters, outputs, configs


def get_inputs(config_yaml_path):
    spec = yaml.load(config_yaml_path.open(), Loader=Loader)
    inputs = spec[INPUTS_KEY] if INPUTS_KEY in spec else {}
    return inputs


def get_outputs_mic(config_yaml_path):
    spec = yaml.load(config_yaml_path.open(), Loader=Loader)
    outputs = spec[OUTPUTS_KEY] if OUTPUTS_KEY in spec else {}
    return outputs


def get_parameters(config_yaml_path):
    spec = yaml.load(config_yaml_path.open(), Loader=Loader)
    parameters = spec[PARAMETERS_KEY] if PARAMETERS_KEY in spec else {}
    return parameters


def get_configs(config_yaml_path):
    spec = yaml.load(config_yaml_path.open(), Loader=Loader)
    configs = spec[CONFIG_FILE_KEY] if CONFIG_FILE_KEY in spec else {}
    return configs

def get_framework(config_yaml_path):
    spec = yaml.load(config_yaml_path.open(), Loader=Loader)
    framework = spec[FRAMEWORK_KEY] if FRAMEWORK_KEY in spec else None
    return framework

def get_code(config_yaml_path):
    spec = yaml.load(config_yaml_path.open(), Loader=Loader)
    code = spec[CODE_KEY] if CODE_KEY in spec else {}
    return code

def create_file_yaml_basic(config_yaml_path: Path):
    make_yaml(config_yaml_path)
