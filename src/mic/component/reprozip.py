import re
from pathlib import Path
from typing import List
import logging
import click
from mic.config_yaml import slugify
from mic.constants import *
import shlex
from mic._utils import get_mic_logger
import os

logging = get_mic_logger()
default_path = Path(MIC_DEFAULT_PATH)


def relative(files: List[Path], user_execution_directory):
    response = {}
    for i in files:
        path = Path(i).relative_to(user_execution_directory)
        name = slugify(str(path.name).replace('.', "_"))

        response[name] = {
            PATH_KEY: str(path),
            FORMAT_KEY: str(path.suffix).replace('.', '')
        }
    return response


def get_inputs_outputs_reprozip(spec, user_execution_directory, aggregrate=True):
    inputs = []
    inputs_outputs_ = spec[REPRO_ZIP_INPUTS_OUTPUTS] if spec[REPRO_ZIP_INPUTS_OUTPUTS] else []
    for i in inputs_outputs_:
        key_ = i[PATH_KEY]
        if default_path in Path(key_).parents:
            parts = Path(key_).relative_to(default_path).parts
            if isinstance(parts, str):
                inputs.append(key_)
            elif isinstance(parts, tuple):
                inputs.append(str(user_execution_directory / parts[0]))

    other_files_ = spec[REPRO_ZIP_OTHER_FILES] if spec[REPRO_ZIP_OTHER_FILES] else []
    for i in other_files_:
        if default_path in Path(i).parents:
            parts = Path(i).relative_to(default_path).parts
            if isinstance(parts, str):
                inputs.append(i)
            elif isinstance(parts, tuple) and aggregrate:
                inputs.append(str(user_execution_directory / parts[0]))
            elif isinstance(parts, tuple) and not aggregrate:
                inputs.append(str(user_execution_directory / Path(i).relative_to(default_path)))

    return list(set(inputs))


def get_outputs_reprozip(spec, user_execution_directory, aggregrate=False):
    """

    :param spec:
    :type spec:
    """
    outputs = []
    repro_zip_outputs = spec[OUTPUTS_KEY] if spec[OUTPUTS_KEY] else []
    for i in repro_zip_outputs:
        if default_path in Path(i).parents:
            parts = Path(i).relative_to(default_path).parts
            if isinstance(parts, str) and not aggregrate:
                outputs.append(i)
            if isinstance(parts, tuple):
                if aggregrate:
                    outputs.append(str(user_execution_directory / parts[0]))
                else:
                    outputs.append(str(user_execution_directory / Path(i).relative_to(default_path)))
    return list(set(outputs))


def get_parameters_reprozip(spec, reprozip_spec):
    run_lines = ''
    for rep_run in reprozip_spec[REPRO_ZIP_RUNS]:

        # Adds quotes around any cell that contains a space
        quoted_run = []
        for i in rep_run[REPRO_ZIP_ARGV]:
            if " " in i:
                quoted_run.append(f"\"{i}\"")
            else:
                quoted_run.append(i)

        run_lines = " ".join(map(str, quoted_run)).splitlines()

    params_added = 0
    for line in run_lines:
        # capture invocation line(s)
        start_pos = line.find("./")
        if start_pos >= 0:
            invocation_split = shlex.split(line[start_pos:len(line)])
            invocation_split = invocation_split[1:len(invocation_split)]
            for i in invocation_split:
                the_type = ""
                # check if there is a . in the line. This means it could be a file extension or float
                is_param = False

                if i.find(".") != -1:
                    try:
                        float(i)
                        is_param = True
                        the_type = "float"

                    except ValueError:
                        # i is a file (file.txt)
                        pass

                if the_type == "":
                    try:
                        # i is an int
                        int(i)
                        the_type = "int"
                        is_param = True
                    except ValueError:
                        # Not a parameter if it starts with a hyphen (--option) or exists as a file (inputs.csv)
                        if i.find("-") != 0 and not os.path.exists(i):
                            # not a parameter if it is already an input or output
                            is_io = False

                            if INPUTS_KEY in spec:
                                if i.replace(".","_") in spec[INPUTS_KEY].keys():
                                    is_io = True

                            if OUTPUTS_KEY in spec:
                               if i.replace(".","_") in spec[OUTPUTS_KEY].keys():
                                   is_io = True

                            if not is_io:
                                # i is a string
                                the_type = "str"
                                is_param = True

                if is_param:
                    params_added += 1
                    auto_name = "param_" + str(params_added)
                    spec[PARAMETERS_KEY].update({auto_name: {NAME_KEY: "", DEFAULT_VALUE_KEY: i,
                                                             DATATYPE_KEY: the_type,
                                                             DEFAULT_DESCRIPTION_KEY: ""}})
                    click.echo("Adding \"{}\" from value {}".format(auto_name, i))
                    logging.debug("Adding parameter: {}".format(auto_name))

            if params_added > 0:
                click.secho("The parameters of the model component are available in the mic directory.", fg="green")
            else:
                click.secho("No parameters found", fg="green")
                logging.info("No parameters added")

            return spec

def generate_pre_runner(spec, user_execution_directory):
    code = ""
    paths = []
    code_items = spec[CODE_KEY] if CODE_KEY in spec and spec[CODE_KEY] else {}
    try:
        for key, file in code_items.items():
            paths.append(Path(file[PATH_KEY]))

        inputs_items = spec[INPUTS_KEY] if INPUTS_KEY in spec and spec[INPUTS_KEY] else {}
        items = inputs_items.items()
        for key, file in items:
            paths.append(Path(file[PATH_KEY]))

        for path in paths:
            parts = path.parts
            if isinstance(parts, tuple) and len(parts) > 1:
                code = f"""{code}
cp -rv {path.name} {str(path)}"""
        logging.debug("Pre runner code: {}".format(repr(code)))
        return code
    except KeyError as e:
        click.secho("Error: Malformed yaml. {} is missing expected fields".format(CONFIG_YAML_NAME),fg ="red")
        logging.error("Error: Malformed yaml")
        logging.error(e)
        click.secho(e,fg ="yellow")

        
def generate_runner(spec, user_execution_directory, mic_inputs, mic_outputs, mic_parameters):
    code = ''

    for run in spec[REPRO_ZIP_RUNS]:

        # Adds quotes around any cell that contains a space
        quoted_run = []
        for i in run[REPRO_ZIP_ARGV]:
            if " " in i:
                quoted_run.append(f"\"{i}\"")
            else:
                quoted_run.append(i)

        code_line = ' '.join(map(str, quoted_run))
        code_line = format_code(code_line, mic_inputs, mic_outputs, mic_parameters)
        dir_ = str(Path(run[REPRO_ZIP_WORKING_DIR]).relative_to(default_path))
        code = f"""{code}
pushd {dir_}
{code_line}
popd"""
    logging.debug("Runner code: {}".format(repr(code)))
    return code

  
def format_code(code, mic_inputs, mic_outputs, mic_parameters):
    """
    Replaces any reference to inputs and outputs with the variable name of the yaml reference
    Ex:
    ./my_script.py -i inp.txt -p 4 -o out.txt
    Becomes:
    ./my_script.py -i ${inp_txt} -p ${param_1} -o ${out_txt}
    Note: this works by checking if a input/output on the command like matches an i/o from the yaml
    :param code:
    :param mic_inputs:
    :param mic_outputs:
    :param mic_parameters:
    :return:
    """

    data = [mic_inputs,mic_outputs]
    code = shlex.split(code)
    new_code = []
    known_bad_keys = []
    for item in code:
        edit = False
        # Appends tag to inputs and outputs
        for d in data:
            for key in d:
                try:
                    if str((d[key])['path'].lower()) == item.lower():
                        new_code.append("${" + key + "}")
                        edit = True
                except KeyError:
                    # Prevents the same bad keys from being repeated
                    if key not in known_bad_keys:
                        logging.warning("Warning: No path found for {}".format(key))
                        click.secho("No path found for: {}".format(key),fg="yellow")
                        known_bad_keys.append(key)

        if not edit:
            # appends tag to parameters
            for key in mic_parameters:
                try:
                    if (mic_parameters[key])["default_value"] == item:

                        # Check if param is a str. If it is add quotes around it
                        if (mic_parameters[key])["type"] == "str":
                            new_code.append("\"${" + key + "}\"")
                        else:
                            new_code.append("${" + key + "}")

                        edit = True
                except KeyError:
                    if key not in known_bad_keys:
                        click.secho("Warning: Could not check default value for {}".format(key),fg="yellow")
                        logging.warning("Could not check default value for: {}".format(key))
                        known_bad_keys.append(key)
        if not edit:
            new_code.append(item)


    return " ".join(new_code)


def find_code_files(spec, inputs, config_files, user_execution_directory):
    code_files = []
    for run in spec[REPRO_ZIP_RUNS]:

        if "binary" in run:
            try:
                code_files.append(str(user_execution_directory / Path(run['binary']).relative_to(default_path)))
            except ValueError:
                pass

        for _input in inputs:
            argv = run[REPRO_ZIP_ARGV] if isinstance(run[REPRO_ZIP_ARGV], list) else run[REPRO_ZIP_ARGV].split(' ')
            for arg in argv:
                files_path = Path(_input)
                if files_path.name in arg \
                        and files_path.is_file() \
                        and str(files_path) not in config_files:
                    # If file is a known executable add it to code_files. Else ask user if it is executable
                    if is_executable(files_path):
                        code_files.append(_input)
                        click.echo("Adding {} as executable".format(files_path.name))
                        logging.debug("Adding executable: {}".format(files_path.name))
    return list(set(code_files))


def is_executable(file_path):

    ext = os.path.splitext(file_path)[-1] # Only grab the extension
    print(ext)
    if ext.lower() in EXECUTABLE_EXTENSIONS:
        return True
    else:
        return False


def extract_parameters_from_command(command_line):
    regex = r"(\"[^\"]+\"|[^\s\"]+)"
    matches = re.finditer(regex, command_line, re.IGNORECASE)
    for matchNum, match in enumerate(matches, start=2):
        print(match.group())
