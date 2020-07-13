import re
from pathlib import Path
from typing import List

import click
from mic.config_yaml import slugify
from mic.constants import *

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


def generate_pre_runner(spec, user_execution_directory):
    code = ""
    paths = []
    code_items = spec[CODE_KEY] if CODE_KEY in spec and spec[CODE_KEY] else {}
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
    return code


def generate_runner(spec, user_execution_directory, mic_inputs, mic_outputs):
    code = ''

    for run in spec[REPRO_ZIP_RUNS]:
        code_line = ' '.join(map(str, run[REPRO_ZIP_ARGV]))
        code_line = format_code(code_line, mic_inputs, mic_outputs)
        dir_ = str(Path(run[REPRO_ZIP_WORKING_DIR]).relative_to(default_path))
        code = f"""{code}
pushd {dir_}
{code_line}
popd"""
    return code

def format_code(code, mic_inputs, mic_outputs):
    """
    Replaces any reference to inputs and outputs with the variable name of the yaml reference
    Ex:
    ./my_script.py -i inp.txt -p 4 -o out.txt
    Becomes:
    ./my_script.py -i ${inp_txt} -p 4 -o ${out_txt}
    Note: this works by checking if a input/output on the command like matches an i/o from the yaml
    :param code:
    :param mic_inputs:
    :param mic_outputs:
    :return:
    """
    code = code.split(" ")
    new_code = []
    for item in code:
        edit = False
        for key in mic_inputs:
            check = item.replace(".", "_")
            if str(key.lower()) == (check.lower()):
                new_code.append("${" + key + "}")
                edit = True
        for key in mic_outputs:
            check = item.replace(".", "_")
            if str(key.lower()) == (check.lower()):
                new_code.append("${" + key + "}")
                edit = True

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
                    elif click.confirm(f"Is {files_path} an executable script/program?", default=False):
                        code_files.append(_input)
    return list(set(code_files))

def is_executable(file_path):

    for i in EXECUTABLE_EXTENSIONS:
        name = file_path.name.lower()
        name = "." + (name.split("."))[1]
        if i.lower() == name.lower():
            return True

    return False

def extract_parameters_from_command(command_line):
    regex = r"(\"[^\"]+\"|[^\s\"]+)"
    matches = re.finditer(regex, command_line, re.IGNORECASE)
    for matchNum, match in enumerate(matches, start=2):
        print(match.group())
