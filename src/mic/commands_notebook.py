from pathlib import Path

import click
import semver

import mic
from mic import _utils
from mic._utils import get_mic_logger
from mic.component.initialization import render_bash_color, render_run_sh, render_io_sh, render_output
from mic.component.reprozip import format_code
from mic.config_yaml import get_spec, create_config_file_yaml, write_spec
from mic.constants import DOCKER_KEY

from mic.config_yaml import get_parameters as mic_get_parameters
from mic.config_yaml import get_inputs as mic_get_inputs
from mic.config_yaml import get_outputs_mic as mic_get_outputs

from mic.cwl.cwl import get_parameters, add_parameters, add_outputs, supported, get_base_command, get_docker_image, \
    get_inputs, add_inputs

logging = get_mic_logger()


@click.group()
@click.option("--verbose", "-v", default=0, count=True)
def cli(verbose):
    _utils.init_logger()
    try:
        lv = ".".join(_utils.get_latest_version().split(".")[:3])
    except Exception as e:
        click.secho(
            f"""WARNING: Unable to check if MIC is updated""",
            fg="yellow",
        )
        return

    cv = ".".join(mic.__version__.split(".")[:3])

    if semver.compare(lv, cv) > 0:
        click.secho(
            f"""WARNING: You are using mic version {mic.__version__}, however version {lv} is available.
You should consider upgrading via 'pip install --upgrade mic' command.""",
            fg="yellow",
        )

@cli.command(short_help="Expect a cwl definition a values")
@click.argument(
    "spec_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    required=True
)

@click.argument(
    "values_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    required=True
)
def cwl(spec_file, values_file):
    mic_dir = Path('.')
    mic_config_path = create_config_file_yaml(mic_dir)
    cwl_spec = get_spec(Path(spec_file))
    cwl_values = get_spec(Path(values_file))

    supported(cwl_spec)
    cwl_line = get_base_command(cwl_spec)
    docker_image = get_docker_image(cwl_spec)

    parameters = get_parameters(cwl_spec)
    inputs = get_inputs(cwl_spec)
    outputs = cwl_spec["outputs"]
    for key, item in parameters.items():
        cwl_line = f"{cwl_line} {item['inputBinding']['prefix']} {cwl_values[key]}"

    add_inputs(mic_config_path, inputs, cwl_values)
    add_outputs(mic_config_path, outputs, cwl_values)
    add_parameters(mic_config_path, parameters, cwl_values)
    mic_inputs = mic_get_inputs(mic_config_path)
    mic_outputs = mic_get_outputs(mic_config_path)
    mic_parameters = mic_get_parameters(mic_config_path)
    print(cwl_line)
    code = format_code(cwl_line, mic_inputs, mic_outputs, mic_parameters)
    print(code)
    write_spec(mic_config_path, DOCKER_KEY, docker_image)
    mic_directory_path = mic_config_path.parent

    render_bash_color(mic_directory_path)
    render_run_sh(mic_directory_path, mic_inputs, mic_parameters, mic_outputs, code)
    render_io_sh(mic_directory_path, mic_inputs, mic_parameters, {})
    render_output(mic_directory_path, mic_outputs, False)
    #print(parameters)
    pass