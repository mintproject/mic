import re
from pathlib import Path
from typing import List

from mic.config_yaml import slugify
from mic.constants import *

default_path = Path(MIC_DEFAULT_PATH)


def convert_reprozip_to_mic():
    pass


def relative(files: List[Path], user_execution_directory):
    response = {}
    for i in files:
        path = Path(i).relative_to(user_execution_directory)
        name = slugify(str(path.name).replace('.', "_"))

        response[name] = {
            PATH_KEY: str(path.name),
            FORMAT_KEY: str(path.suffix).replace('.', '')
        }
    return response


def get_inputs(spec, user_execution_directory, aggregrate=True):
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


def get_outputs(spec, user_execution_directory, aggregrate=False):
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
    code = ''
    paths = []
    for key, file in spec[CODE_KEY].items():
        paths.append(Path(file[PATH_KEY]))

    for key, file in spec[INPUTS_KEY].items():
        paths.append(Path(file[PATH_KEY]))

    for path in paths:
        parts = path.parts
        if isinstance(parts, tuple) and len(parts) > 1:
            code = f"""{code}
cp -rv {path.name} {str(path)}"""
    return code


def generate_runner(spec, user_execution_directory):
    code = ''
    for run in spec[REPRO_ZIP_RUNS]:
        dir_ = str(Path(run[REPRO_ZIP_WORKING_DIR]).relative_to(default_path))
        code = f"""{code}
pushd {dir_}
{' '.join(map(str, run[REPRO_ZIP_ARGV]))}
popd"""
    return code


def find_code_files(spec, inputs, config_files):
    code_files = []
    for run in spec[REPRO_ZIP_RUNS]:
        for _input in inputs:
            argv = run[REPRO_ZIP_ARGV] if isinstance(run[REPRO_ZIP_ARGV], list) else run[REPRO_ZIP_ARGV].split(' ')
            for arg in argv:
                files_path = Path(_input)
                if files_path.name in arg and files_path.suffix not in [".txt", ".json", "*.png"]:
                    code_files.append(_input)

    return list(set(code_files))


def extract_parameters_from_command(command_line):
    regex = r"(\"[^\"]+\"|[^\s\"]+)"
    matches = re.finditer(regex, command_line, re.IGNORECASE)
    for matchNum, match in enumerate(matches, start=2):
        print(match.group())
