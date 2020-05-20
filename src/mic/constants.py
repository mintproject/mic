from enum import Enum

CONFIG_FILE = "config.json"
CONFIG_YAML_NAME = "config.yaml"
INPUTS_KEY = "inputs"
PARAMETERS_KEY = "parameters"
CONFIG_FILE_KEY = "configs"
STEP_KEY = "step"
OUTPUTS_KEY = "outputs"
NAME_KEY = "name"
PATH_KEY = "path"
DEFAULT_VALUE_KEY = "default_value"
DATA_DIRECTORY_NAME = "data"
RUN_FILE = "run"
IO_FILE = "io.sh"
OUTPUT_FILE = "output.sh"
DOCKER_FILE = "Dockerfile"
SRC_DIR = "src"
DOCKER_DIR = "docker"
DATA_DIR = "data"
REQUIREMENTS_FILE = "requirements.txt"
EXECUTIONS_DIR = "executions"
TOTAL_STEPS = 8

class Framework(Enum):
    PYTHON37 = ("python37", "mintproject/python37:20.5.1")
    CONDA = ("conda", "mintproject/conda:20.5.1")
    GENERIC = ("generic", "mintproject/generic:20.5.1")

    def __init__(self, label, image):
        self.label = label
        self.image = image

    def __str__(self):
        return self.label


def handle(value):
    for i in Framework:
        if value == i.label:
            return i
