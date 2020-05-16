import os

from click.testing import CliRunner
from yaml import load

from mic.__main__ import step1, step2
from mic.config_yaml import get_numbers_inputs_parameters
from mic.constants import *

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

MODEL_NAME = "model"
PARAMETERS_2: int = 2


def test_skeleton(tmp_path):
    runner = CliRunner()
    os.chdir(tmp_path)
    try:
        response = runner.invoke(step1, [MODEL_NAME])
        assert response.exit_code == 0
    except:
        assert False


def test_init(tmp_path):
    runner = CliRunner()
    os.chdir(tmp_path)
    response = runner.invoke(step1, [MODEL_NAME])
    component_dir = tmp_path / MODEL_NAME
    p = component_dir / DATA_DIRECTORY_NAME / "hello.txt"
    p.write_text("test")
    try:
        response = runner.invoke(step2, [MODEL_NAME, "-p", PARAMETERS_2])
        assert response.exit_code == 0
    except:
        assert False
    spec = load((component_dir / CONFIG_YAML_NAME).open(), Loader=Loader)
    assert len(spec["inputs"]) == 1
    assert len(spec["parameters"]) == 2


def test_init_two_inputs(tmp_path):
    runner = CliRunner()
    os.chdir(tmp_path)
    response = runner.invoke(step1, [MODEL_NAME])
    component_dir = tmp_path / MODEL_NAME
    p = component_dir / DATA_DIRECTORY_NAME / "hello.txt"
    p.write_text("test")

    p2 = component_dir / DATA_DIRECTORY_NAME / "hello2.txt"
    p2.write_text("test")

    try:
        response = runner.invoke(step2, [MODEL_NAME, "-p", PARAMETERS_2])
        assert response.exit_code == 0
    except:
        assert False
    spec = load((component_dir / CONFIG_YAML_NAME).open(), Loader=Loader)
    assert len(spec["inputs"]) == 2
    assert len(spec["parameters"]) == 2


def test_init_two_inputs_zero_parameters(tmp_path):
    runner = CliRunner()
    os.chdir(tmp_path)
    response = runner.invoke(step1, ["-n", MODEL_NAME])
    component_dir = tmp_path / MODEL_NAME
    p = component_dir / DATA_DIRECTORY_NAME / "hello.txt"
    p.write_text("test")

    p2 = component_dir / DATA_DIRECTORY_NAME / "hello2.txt"
    p2.write_text("test")

    try:
        response = runner.invoke(step2, [MODEL_NAME])
        assert response.exit_code == 0
    except:
        assert False
    spec = load((component_dir / CONFIG_YAML_NAME).open(), Loader=Loader)
    assert len(spec[INPUTS_KEY]) == 2
    assert PARAMETERS_KEY not in spec


def test_init_two_inputs_zero_parameters(tmp_path):
    runner = CliRunner()
    os.chdir(tmp_path)
    response = runner.invoke(step1, [MODEL_NAME])
    component_dir = tmp_path / MODEL_NAME
    p = component_dir / DATA_DIRECTORY_NAME / "hello.txt"
    p.write_text("test")

    p2 = component_dir / DATA_DIRECTORY_NAME / "hello_dir"
    p2.mkdir()
    p3 = p2 / "hello.txt"
    p3.write_text("test")

    try:
        response = runner.invoke(step2, [MODEL_NAME])
        assert response.exit_code == 0
    except:
        assert False

    number_inputs, number_parameters, number_outputs = get_numbers_inputs_parameters(component_dir / CONFIG_YAML_NAME)
    assert number_inputs == 2
    assert number_parameters == 0