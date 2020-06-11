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


def get_outputs(spec):
    """

    :param spec:
    :type spec:
    """
    return spec[OUTPUTS_KEY]
