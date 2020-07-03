import shutil
from os import fdopen
from pathlib import Path
from tempfile import mkstemp

from click.testing import CliRunner
from mic.config_yaml import get_parameters, get_inputs, get_configs, get_outputs_mic
from mic.click_encapsulate.commands import inputs, add_parameters, configs, outputs, wrapper, run
from mic.constants import MIC_DIR, CONFIG_YAML_NAME

RESOURCES = "resources"
mic_1 = Path(__file__).parent / RESOURCES / "mic_full.yaml"
mic_empty = Path(__file__).parent / RESOURCES / "mic_empty.yaml"


def test_issue_185(tmp_path):
    """
    Test case for:
        1 input
        1 output

    :param tmp_path:
    :return:
    """

    test_name = "185"

    temp_test = tmp_path / test_name
    mic_dir = temp_test / MIC_DIR
    mic_config_arg = str(mic_dir / CONFIG_YAML_NAME)

    path_test_name = tmp_path / test_name
    path = Path(__file__).parent / RESOURCES / test_name
    shutil.copytree(path, path_test_name)
    runner = CliRunner()
    cmd_add_parameters(mic_config_arg, runner)
    check_parameters(mic_config_arg)
    cmd_inputs(mic_config_arg, runner)
    check_inputs(mic_config_arg)
    cmd_outputs(mic_config_arg, runner)
    check_outputs(mic_config_arg)
    cmd_wrapper(mic_config_arg, runner)
    cmd_run(mic_config_arg, runner)


def check_parameters(mic_config_arg):
    parameters = get_parameters(Path(mic_config_arg))
    assert parameters == {'add': {'default_value': 12.0, 'description': '', 'type': 'float'}}


def cmd_add_parameters(mic_config_arg, runner):
    parameters = {"add": 12}
    for key, value in parameters.items():

        result = runner.invoke(add_parameters, ["-f", mic_config_arg, "--name", key, "--value", value],
                               catch_exceptions=False)
        print(result.output)
        assert result.exit_code == 0


def cmd_inputs(mic_config_arg, runner):

    result = runner.invoke(inputs, ["-f", mic_config_arg], input='Y', catch_exceptions=False)
    print(result.output)
    assert result.exit_code == 0


def check_inputs(mic_config_arg):
    _inputs = get_inputs(Path(mic_config_arg))
    assert _inputs == {'in_txt': {'format': 'txt', 'path': 'in.txt'},
                       'outputs_zip': {'format': 'zip', 'path': 'outputs.zip'}}


def cmd_outputs(mic_config_arg, runner):
    result = runner.invoke(outputs, ["-f", mic_config_arg], catch_exceptions=False)
    print(result.output)
    assert result.exit_code == 0


def check_outputs(mic_config_arg):
    files = get_outputs_mic(Path(mic_config_arg))
    assert files == {'out_txt': {'format': 'txt', 'path': 'outputs/out.txt'}}


def cmd_wrapper(mic_config_arg, runner):
    result = runner.invoke(wrapper, ["-f", mic_config_arg], catch_exceptions=False)
    print(result.output)
    assert result.exit_code == 0


def cmd_run(mic_config_arg, runner):

    result = runner.invoke(run, ["-f", mic_config_arg], catch_exceptions=False)
    print(result.output)
    assert result.exit_code == 0

