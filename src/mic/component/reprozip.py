import re
from pathlib import Path

from mic.constants import *

DEFAULT_PATH = "/tmp/mint/"


def convert_reprozip_to_mic():
    pass


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
