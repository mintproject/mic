import re
from pathlib import Path
from typing import List

from mic.constants import *

def convert_reprozip_to_mic():
    pass


def relative(files: List[Path]):
    response = {}
    for i in files:
        path = Path(i).relative_to(Path(DEFAULT_PATH))
        response[path.name] = {
            PATH_KEY: str(path),
            'format': str(path.suffix)
        }
    return response


def get_inputs(spec):
    default_path = Path(DEFAULT_PATH)
    inputs = []

    outputs_ = spec[REPRO_ZIP_INPUTS_OUTPUTS] if spec[REPRO_ZIP_INPUTS_OUTPUTS] else []
    for i in outputs_:
        if default_path in Path(i).parents:
            inputs.append(i)

    other_files_ = spec[REPRO_ZIP_OTHER_FILES] if spec[REPRO_ZIP_OTHER_FILES] else []
    for i in other_files_:
        if default_path in Path(i).parents:
            inputs.append(i)
    return inputs


def generate_runner(spec):
    code = ''
    for run in spec[REPRO_ZIP_RUNS]:
        code = f"""{code}
pushd {run[REPRO_ZIP_WORKING_DIR]}
{' '.join(map(str, run[REPRO_ZIP_ARGV]))}
popd"""
    return code


def find_code_files(spec, inputs):
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


def get_outputs(spec):
    """

    :param spec:
    :type spec:
    """
    return spec[OUTPUTS_KEY]
