from enum import Enum

CONFIG_FILE = "config.json"
CONFIG_YAML_NAME = "mic.yaml"
INPUTS_KEY = "inputs"
PARAMETERS_KEY = "parameters"
CONFIG_FILE_KEY = "configs"
STEP_KEY = "step"
OUTPUTS_KEY = "outputs"
NAME_KEY = "name"
DEFAULT_DESCRIPTION_KEY = "description"
PATH_KEY = "path"
DEFAULT_VALUE_KEY = "default_value"
DATA_DIRECTORY_NAME = "data"
RUN_FILE = "run"
IO_FILE = "io.sh"
OUTPUT_FILE = "output.sh"
DOCKER_FILE = "Dockerfile"
SRC_DIR = "src"
DOCKER_DIR = "docker"
MIC_CONFIG_FILE_NAME = "MIC configuration file"
DATA_DIR = "data"
REQUIREMENTS_FILE = "requirements.txt"
EXECUTIONS_DIR = "executions"
TOTAL_STEPS = 8
MINT_COMPONENT_ZIP = "mint_component"
GIT_TOKEN_KEY = "git_token"
GIT_USERNAME_KEY = "git_username"
DOCKER_KEY = "docker_image"
LAST_EXECUTION_DIR = "last_execution_dir"
REPO_KEY = "github_repo_url"
VERSION_KEY = "version"
DOCKER_USERNAME_KEY = "dockerhub_username"
MINT_COMPONENT_KEY = "mint_component_url"
MINT_INSTANCE = "https://w3id.org/okn/i/mint/"

TYPE_PARAMETER = "https://w3id.org/okn/o/sd#Parameter"
TYPE_MODEL_CONFIGURATION = "https://w3id.org/okn/o/sdm#ModelConfiguration"
TYPE_DATASET = "https://w3id.org/okn/o/sd#DatasetSpecification"
TYPE_SOFTWARE_IMAGE = "https://w3id.org/okn/o/sd#SoftwareImage"
TYPE_SOFTWARE_VERSION = "https://w3id.org/okn/o/sd#SoftwareVersion"
GITIGNORE_FILE = ".gitignore"
DEFAULT_PARAMETER_COMMENT = "# value added by MIC. Replace with your own default value"
DEFAULT_DESCRIPTION_MESSAGE = "# insert description left of this comment"

class Framework(Enum):
    PYTHON37 = ("python37", "mintproject/python37:20.5.1")
    CONDA = ("conda", "mintproject/conda:20.5.1")
    GENERIC = ("general", "mintproject/generic:20.5.1")

    def __init__(self, label, image):
        self.label = label
        self.image = image

    def __str__(self):
        return self.label


def handle(value):
    for i in Framework:
        if value == i.label:
            return i
