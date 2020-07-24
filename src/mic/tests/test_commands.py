import io
import os
import shutil
from pathlib import Path

from click.testing import CliRunner
from mic.click_encapsulate.commands import add_parameters, DATATYPE_KEY, start, trace
from mic.config_yaml import get_parameters, get_spec

RESOURCES = "resources"


def test_add_parameters(tmpdir):
    runner = CliRunner()
    mic_file = Path(__file__).parent / RESOURCES / "mic_parameters.yaml"
    mic_file = shutil.copy(mic_file, tmpdir / mic_file.name)
    try:
        result = runner.invoke(add_parameters, ["-f", str(mic_file), "--name", "a", "--value", "test"],
                               catch_exceptions=False)
    except Exception as e:
        print(e)
        assert False
    assert result.exit_code == 0
    assert get_parameters(mic_file)["a"]["default_value"] == "test"


def test_add_parameters_exit1(tmpdir):
    runner = CliRunner()
    mic_file = Path(__file__).parent / RESOURCES / "mic_parameters.yaml"
    mic_file = shutil.copy(mic_file, tmpdir / mic_file.name)
    try:
        result = runner.invoke(add_parameters, ["-f", str(mic_file), "--name", "a", "--value", "b"],
                               catch_exceptions=False)
        result = runner.invoke(add_parameters, ["-f", str(mic_file), "--name", "a", "--value", "b"],
                               catch_exceptions=False)
    except Exception as e:
        assert False
    print(result.output)
    print(result.exit_code)
    assert result.exit_code == 1


def test_add_parameters_exit0(tmpdir):
    runner = CliRunner()
    mic_file = Path(__file__).parent / RESOURCES / "mic_parameters.yaml"
    mic_file = shutil.copy(mic_file, tmpdir / mic_file.name)
    try:
        result = runner.invoke(add_parameters, ["-f", str(mic_file), "--name", "a", "--value", "b"],
                               catch_exceptions=False)
        result = runner.invoke(add_parameters, ["-f", str(mic_file), "--name", "a", "--value", "b", "--overwrite"],
                               catch_exceptions=False)
    except Exception as e:
        assert False
    assert result.exit_code == 0


def test_add_parameters_float(tmpdir):
    runner = CliRunner()
    mic_file = Path(__file__).parent / RESOURCES / "mic_parameters.yaml"
    mic_file = shutil.copy(mic_file, tmpdir / mic_file.name)
    values = [1.0, -1.0, -.0, .0, '1.0', '-1.0', '-.0', '.0', 0.0, '0.0']
    for index, value in enumerate(values):
        try:
            result = runner.invoke(add_parameters, ["-f", str(mic_file), "--name", index, "--value", value],
                                   catch_exceptions=False)
            print(result.output)
        except Exception as e:
            assert False
        print("CURR: mic_file(",mic_file,") | index(",index, ")")
        print(get_spec(mic_file))
        assert get_parameters(mic_file)[index]["default_value"] == float(value)
        assert get_parameters(mic_file)[index][DATATYPE_KEY] == "float"
        assert result.exit_code == 0


def test_add_parameters_integer(tmpdir):
    runner = CliRunner()
    mic_file = Path(__file__).parent / RESOURCES / "mic_parameters.yaml"
    mic_file = shutil.copy(mic_file, tmpdir / mic_file.name)
    avalues = [-3, 1, 0]
    for index, value in enumerate(avalues):
        try:
            result = runner.invoke(add_parameters, ["-f", str(mic_file), "--name", index, "--value", value],
                                   catch_exceptions=False)
            print(result.output)
        except Exception as e:
            assert False
        assert get_parameters(mic_file)[index]["default_value"] == int(value)
        # assert get_parameters(mic_file)[index][DATATYPE_KEY] == "int"
        assert result.exit_code == 0


def test_start(tmp_path, monkeypatch):
    runner = CliRunner()
    os.chdir(tmp_path)
    monkeypatch.setattr('sys.stdin', io.StringIO("\nexit\n"))
    result = runner.invoke(start, ["--name", "test"], catch_exceptions=False)
    assert result.exit_code == 0


def test_start_image(tmp_path, monkeypatch):
    runner = CliRunner()
    os.chdir(tmp_path)
    monkeypatch.setattr('sys.stdin', io.StringIO("\nexit\n"))
    result = runner.invoke(start, ["--name", "test", "--image", "busybox"], catch_exceptions=False)
    assert result.exit_code == 0


def test_trace(tmp_path, monkeypatch):
    runner = CliRunner()
    os.chdir(tmp_path)
    monkeypatch.setattr('sys.stdin', io.StringIO("\nexit\n"))
    result = runner.invoke(trace, ["ping", "-c", "google.com"], catch_exceptions=False)
    assert result.exit_code == 0
