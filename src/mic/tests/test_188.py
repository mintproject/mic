import shutil
from os import fdopen
from pathlib import Path
from tempfile import mkstemp

from click.testing import CliRunner
from mic.component.initialization import create_base_directories
from mic.config_yaml import get_parameters, get_inputs, get_configs, get_outputs_mic
from mic.click_encapsulate.commands import inputs, add_parameters, configs, outputs, wrapper, run
from mic.constants import MIC_DIR, CONFIG_YAML_NAME, SRC_DIR, DOCKER_DIR, DATA_DIR

RESOURCES = "resources"
mic_1 = Path(__file__).parent / RESOURCES / "mic_full.yaml"
mic_empty = Path(__file__).parent / RESOURCES / "mic_empty.yaml"


def test_issue_188(tmp_path):
    test_name = "188"
    temp_test = tmp_path / test_name
    mic_dir = temp_test / MIC_DIR
    repository_test = Path(__file__).parent / RESOURCES / test_name
    shutil.copytree(repository_test, temp_test)
    runner = CliRunner()


    mic_config_arg = str(mic_dir / CONFIG_YAML_NAME)
    create_base_directories(mic_dir, interactive=False)
    cmd_inputs(mic_config_arg, runner)
    check_inputs(mic_config_arg)
    cmd_outputs(mic_config_arg, runner)
    check_outputs(mic_config_arg)
    cmd_wrapper(mic_config_arg, runner)
    cmd_run(mic_config_arg, runner)


def cmd_start(mic_dir):
    create_base_directories(mic_dir)


def cmd_inputs(mic_config_arg, runner):
    try:
        result = runner.invoke(inputs, ["-f", mic_config_arg], input='N\nN', catch_exceptions=False)
        print(result.output)
    except Exception as e:
        print(e)
        assert False
    assert result.exit_code == 0


def check_inputs(mic_config_arg):
    _inputs = get_inputs(Path(mic_config_arg))
    print("INPUTS: --->",_inputs)
    assert _inputs == {'188_py': {'path': '188.py', 'format': 'py'}, 'sample_input_txt': {'path': 'sample_input.txt', 'format': 'txt'}}


def cmd_outputs(mic_config_arg, runner):
    try:
        result = runner.invoke(outputs, ["-f", mic_config_arg], catch_exceptions=False)
        print(result.output)
    except Exception as e:
        print(e)
        assert False
    assert result.exit_code == 0


def check_outputs(mic_config_arg):
    files = get_outputs_mic(Path(mic_config_arg))
    print(files)
    assert files == {'result_txt': {'path': 'result.txt', 'format': 'txt'}}


def cmd_wrapper(mic_config_arg, runner):
    try:
        result = runner.invoke(wrapper, ["-f", mic_config_arg], catch_exceptions=False)
        print(result.output)
    except Exception as e:
        print(e)
        assert False
    assert result.exit_code == 0


def cmd_run(mic_config_arg, runner):
    try:
        result = runner.invoke(run, ["-f", mic_config_arg], catch_exceptions=False)
        print(result.output)
    except Exception as e:
        print(e)
        assert False
    assert result.exit_code == 0


def replace(file_path, pattern, subst):
    # Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh, 'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    shutil.copymode(file_path, abs_path)
    shutil.remove(file_path)
    shutil.move(abs_path, file_path)
