import shutil
from os import fdopen
from pathlib import Path
from tempfile import mkstemp

from click.testing import CliRunner
from mic.click_encapsulate.commands import inputs, add_parameters, configs, outputs, wrapper, run
from mic.component.initialization import create_base_directories
from mic.config_yaml import get_parameters, get_inputs, get_configs, get_outputs_mic, get_code
from mic.constants import MIC_DIR, CONFIG_YAML_NAME, SRC_DIR, DOCKER_DIR, DATA_DIR

RESOURCES = "resources"


def test_issue_swat(tmp_path):
    """
    Test mic's ability to automatically find and use the mic.yaml file if -f is not provided. This test case is based
    :param tmp_path:
    :return:
    """
    test_name = "swat"
    temp_test = tmp_path / test_name
    mic_dir = temp_test / MIC_DIR
    repository_test = Path(__file__).parent / RESOURCES / test_name
    shutil.copytree(repository_test, temp_test)
    create_base_directories(mic_dir, interactive=False)
    runner = CliRunner()
    mic_config_arg = str(mic_dir / CONFIG_YAML_NAME)
    cmd_configs(mic_config_arg, temp_test, runner)
    check_config(mic_config_arg)
    cmd_inputs(mic_config_arg, runner)
    check_inputs(mic_config_arg)
    check_code(mic_config_arg)
    # cmd_outputs(mic_config_arg, runner)
    # check_outputs(mic_config_arg)
    # cmd_wrapper(mic_config_arg, runner)
    # cmd_run(mic_config_arg, runner)


def cmd_configs(mic_file, path, runner):
    try:
        c1 = str(path / 'TxtInOut' / 'file.cio')
        c2 = str(path / 'TxtInOut' / 'basins.bsn')
        result = runner.invoke(configs, ["-f", str(mic_file), c1, c2], catch_exceptions=False)
        print(result.output)
    except Exception as e:
        print(e)
        assert False
    assert result.exit_code == 0


def check_config(mic_config_arg):
    files = get_configs(Path(mic_config_arg))
    assert files == {'basins_bsn': {'format': 'bsn', 'path': 'TxtInOut/basins.bsn'},
                     'file_cio': {'format': 'cio', 'path': 'TxtInOut/file.cio'}}


def check_parameters(mic_config_arg):
    parameters = get_parameters(Path(mic_config_arg))
    assert parameters == {'a': {'default_value': 5.0, 'type': 'float'}, 'b': {'default_value': 4.0, 'type': 'float'},
                          'c': {'default_value': 6.0, 'type': 'float'}}


def cmd_add_parameters(mic_config_arg, runner):
    parameters = {"a": 5.0, "b": 4.0, "c": 6.0}
    for key, value in parameters.items():
        try:
            result = runner.invoke(add_parameters, ["--name", key, "--value", value],
                                   catch_exceptions=False)
            print(result.output)
        except Exception as e:
            print(e)
            assert False
        assert result.exit_code == 0


def cmd_inputs(mic_file, runner):
    try:
        result = runner.invoke(inputs, ["-f", str(mic_file)], input='Y', catch_exceptions=False)
        print(result.output)
    except Exception as e:
        print(e)
        assert False
    assert result.exit_code == 0


def check_inputs(mic_config_arg):
    _inputs = get_inputs(Path(mic_config_arg))
    assert _inputs == {'txtinout_zip': {'format': 'zip', 'path': 'TxtInOut.zip'}}


def check_code(mic_config_arg):
    _code = get_code(Path(mic_config_arg))
    assert _code == {'swat670': {'format': '', 'path': 'TxtInOut/swat670'}}


def cmd_outputs(mic_config_arg, runner):
    try:
        result = runner.invoke(outputs, catch_exceptions=False)
        print(result.output)
    except Exception as e:
        print(e)
        assert False
    assert result.exit_code == 0


def check_outputs(mic_config_arg):
    files = get_outputs_mic(Path(mic_config_arg))
    assert files == {'a_txt': {'format': 'txt', 'path': 'outputs/a.txt'},
                     'b_txt': {'format': 'txt', 'path': 'outputs/b.txt'},
                     'c_txt': {'format': 'txt', 'path': 'outputs/c.txt'}}


def cmd_wrapper(mic_config_arg, runner):
    try:
        result = runner.invoke(wrapper, catch_exceptions=False)
        print(result.output)
    except Exception as e:
        print(e)
        assert False
    assert result.exit_code == 0


def cmd_run(mic_config_arg, runner):
    try:
        result = runner.invoke(run, catch_exceptions=False)
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


def create_base(path_test_name):
    src = path_test_name / SRC_DIR
    docker = path_test_name / DOCKER_DIR
    data = path_test_name / DATA_DIR
    src.mkdir(parents=True, exist_ok=True)
    docker.mkdir(parents=True, exist_ok=True)
    data.mkdir(parents=True, exist_ok=True)
