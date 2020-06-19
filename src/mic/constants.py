from enum import Enum

GIT_DIRECTORY = ".git"
FORMAT_KEY = "format"
MIC_DEFAULT_PATH = "/tmp/mint/"
REPRO_ZIP_TRACE_DIR = ".reprozip-trace"
REPRO_ZIP_CONFIG_FILE = "config.yml"
REPRO_ZIP_OTHER_FILES = "other_files"
REPRO_ZIP_INPUTS_OUTPUTS = "inputs_outputs"
REPRO_ZIP_RUNS = "runs"
REPRO_ZIP_WORKING_DIR = 'workingdir'
REPRO_ZIP_ARGV = "argv"
MIC_DIR = "mic"
MIC_HIDDEN_DIR = ".mic"
CONFIG_FILE = "config.json"
CONFIG_YAML_NAME = "mic.yaml"
INPUTS_KEY = "inputs"
CODE_KEY = "code_files"
PARAMETERS_KEY = "parameters"
CONFIG_FILE_KEY = "configs"
STEP_KEY = "step"
OUTPUTS_KEY = "outputs"
COMMANDS_RUNNER = "commands"
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
MIC_CONFIG_FILE_NAME = "MIC file"
DATA_DIR = "data"
REQUIREMENTS_FILE = "requirements.txt"
ENVIRONMENT_FILE = "environment.yml"
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
CONDA_YML = "environment.yml"

DEFAULT_PARAMETER_COMMENT = "# value added by MIC. Replace with your own default value"
DEFAULT_DESCRIPTION_MESSAGE = "# insert description left of this comment"

# Default output messages
DEFAULT_CONFIGURATION_WARNING = "WARNING: The profile doesn't exists. To configure it, run:\nmic configure -p"


class Framework(Enum):
    PYTHON37 = ("python3.7", "mintproject/python:3.7", ".py")
    PYTHON38 = ("python3.8", "mintproject/python:3.8", ".py")
    CONDA = ("conda4.7.12", "mintproject/conda:4.7.12", ".py")
    JAVA = ("java8", "mintproject/java:8", ".jar")
    GENERIC = ("general", "mintproject/generic:latest")

    def __init__(self, label, image, extension=None):
        self.label = label
        self.image = image
        self.extension = extension

    def __str__(self):
        return self.label


def handle(value):
    for i in Framework:
        if value == i.label:
            return i
