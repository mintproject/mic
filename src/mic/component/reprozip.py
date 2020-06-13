import re
from pathlib import Path
from typing import List

from mic.constants import *

default_path = Path(MIC_DEFAULT_PATH)


def convert_reprozip_to_mic():
    pass


def relative(files: List[Path]):
    response = {}
    for i in files:
        path = Path(i).relative_to(Path(MIC_DEFAULT_PATH))
        response[path.name] = {
            PATH_KEY: str(path),
            'format': str(path.suffix)
        }
    return response


def get_inputs(spec, aggregrate=True):
    inputs = []
    inputs_outputs_ = spec[REPRO_ZIP_INPUTS_OUTPUTS] if spec[REPRO_ZIP_INPUTS_OUTPUTS] else []
    for i in inputs_outputs_:
        if default_path in Path(i).parents:
            parts = Path(i).relative_to(default_path).parts
            if isinstance(parts, str):
                inputs.append(i)
            elif isinstance(parts, tuple):
                inputs.append(str(default_path / parts[0]))

    other_files_ = spec[REPRO_ZIP_OTHER_FILES] if spec[REPRO_ZIP_OTHER_FILES] else []
    for i in other_files_:
        if default_path in Path(i).parents:
            parts = Path(i).relative_to(default_path).parts
            if isinstance(parts, str):
                inputs.append(i)
            elif isinstance(parts, tuple):
                inputs.append(str(default_path / parts[0]))
    return list(set(inputs))


def generate_pre_runner(spec):
    code = ''
    paths = []
    for key, file in spec[CODE_KEY].items():
        paths.append(Path(file[PATH_KEY]))

    for key, file in spec[INPUTS_KEY].items():
        paths.append(Path(file[PATH_KEY]))

    for path in paths:
        if isinstance(path.parts, tuple):
            code = f"""{code}
cp -rv {path.name} {str(path)}"""
    return code

def generate_runner(spec):
    code = ''
    for run in spec[REPRO_ZIP_RUNS]:
        code = f"""{code}
pushd {run[REPRO_ZIP_WORKING_DIR]}
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


def get_outputs(spec, aggregrate=False):
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
                    outputs.append(str(default_path / parts[0]))
                else:
                    outputs.append(str(i))
    return list(set(outputs))
