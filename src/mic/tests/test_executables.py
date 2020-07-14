import shutil
import os
from pathlib import Path
from tempfile import mkstemp

from click.testing import CliRunner
from mic.component.initialization import create_base_directories
from mic.click_encapsulate.commands import inputs, add_parameters, configs, outputs, wrapper, run, executables
from mic.config_yaml import get_parameters, get_inputs, get_configs, get_outputs_mic,get_code
from mic.constants import *

RESOURCES = "resources"
mic_1 = Path(__file__).parent / RESOURCES / "mic_full.yaml"
mic_empty = Path(__file__).parent / RESOURCES / "mic_empty.yaml"

def test_executables(tmp_path):
    """
    Test case for executables command

    :param tmp_path:
    :return:
    """
    test_name = "test_executables"
    temp_test = tmp_path / test_name
    mic_dir = temp_test / MIC_DIR
    repository_test = Path(__file__).parent / RESOURCES / test_name
    shutil.copytree(repository_test, temp_test)
    create_base_directories(mic_dir, interactive=False)
    runner = CliRunner()
    mic_config_arg = str(mic_dir / CONFIG_YAML_NAME)
    cmd_executables_normal(mic_config_arg, runner)
    check_executables_check(mic_config_arg)
    check_executable_show_after(mic_config_arg,runner)
    cmd_executable_delete(mic_config_arg,runner)
    check_executables_delete_check(mic_config_arg)


def cmd_executables_normal(mic_config_arg, runner):
    try:
        result = runner.invoke(executables,["-f", str(mic_config_arg),
                                            os.path.join("/tmp/mydir/test_executables0/test_executables/a.jar"),
                                            os.path.join("/tmp/mydir/test_executables0/test_executables/tmp/sdsd.exe")],
                               catch_exceptions=False)
        print(result.output)
    except Exception as e:
        print(e)
        assert False
    assert result.exit_code == 0

def check_executables_check(mic_config_arg):
    _code = get_code(Path(mic_config_arg))
    assert _code == {'a_jar': {'format': 'jar', 'path': 'a.jar'},
                     'addtoarray_sh': {'format': 'sh', 'path': 'addtoarray.sh'},
                     'sdsd_exe': {'format': 'exe', 'path': 'tmp/sdsd.exe'}}


def check_executable_show_after(mic_config_arg, runner):
    try:
        result = runner.invoke(executables,["-f", str(mic_config_arg), "--show"], catch_exceptions=False)
        print(result.output)
    except Exception as e:
        print(e)
        assert False
    assert result.exit_code == 0


def cmd_executable_delete(mic_config_arg, runner):
    try:
        result = runner.invoke(executables,["-f", str(mic_config_arg),
                                            os.path.join("/tmp/mydir/test_executables0/test_executables/tmp/sdsd.exe"),
                                            os.path.join("/tmp/mydir/test_executables0/test_executables/addtoarray.sh"),
                                            "--remove"], catch_exceptions=False)
        print(result.output)
    except Exception as e:
        print(e)
        assert False
    assert result.exit_code == 0


def check_executables_delete_check(mic_config_arg):
    _code = get_code(Path(mic_config_arg))
    assert _code == {'a_jar': {'format': 'jar', 'path': 'a.jar'}}