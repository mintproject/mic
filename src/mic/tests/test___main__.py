import logging
import os

from click.testing import CliRunner
from mic.__main__ import step1, step2, step3, step4, step5
from mic.config_yaml import get_numbers_inputs_parameters
from mic.constants import *
from yaml import load

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

MODEL_NAME = "model"
PARAMETERS_2: int = 2


def test_step1(tmp_path):
    runner = CliRunner()
    os.chdir(tmp_path)
    try:
        response = runner.invoke(step1, [MODEL_NAME])
        assert response.exit_code == 0
    except:
        assert False


def test_step2(tmp_path):
    runner = CliRunner()
    os.chdir(tmp_path)
    response = runner.invoke(step1, [MODEL_NAME])
    component_dir = tmp_path / MODEL_NAME
    p = component_dir / DATA_DIRECTORY_NAME / "hello.txt"
    p.write_text("test")
    try:
        response = runner.invoke(step2, ["-f", component_dir / CONFIG_YAML_NAME, "-p", 2])
        assert response.exit_code == 0
    except:
        assert False
    spec = load((component_dir / CONFIG_YAML_NAME).open(), Loader=Loader)
    number_inputs, number_parameters, number_outputs = get_numbers_inputs_parameters(component_dir / CONFIG_YAML_NAME)
    assert number_inputs == 1
    assert number_parameters == 2



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
        response = runner.invoke(step2, ["-f", component_dir / CONFIG_YAML_NAME])
        assert response.exit_code == 0
    except:
        assert False
    spec = load((component_dir / CONFIG_YAML_NAME).open(), Loader=Loader)
    number_inputs, number_parameters, number_outputs = get_numbers_inputs_parameters(component_dir / CONFIG_YAML_NAME)
    assert number_inputs == 2
    assert number_parameters == 0



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
        response = runner.invoke(step2, ["-f", component_dir / CONFIG_YAML_NAME])
        assert response.exit_code == 0
    except:
        assert False
    number_inputs, number_parameters, number_outputs = get_numbers_inputs_parameters(component_dir / CONFIG_YAML_NAME)
    assert number_inputs == 2
    assert number_parameters == 0


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
        response = runner.invoke(step2, ["-f", component_dir / CONFIG_YAML_NAME])
        assert response.exit_code == 0
    except:
        assert False

    number_inputs, number_parameters, number_outputs = get_numbers_inputs_parameters(component_dir / CONFIG_YAML_NAME)
    assert number_inputs == 2
    assert number_parameters == 0


def test_step3(tmp_path):
    runner = CliRunner()
    os.chdir(tmp_path)
    response = runner.invoke(step1, [MODEL_NAME])
    component_dir = tmp_path / MODEL_NAME
    p = component_dir / DATA_DIRECTORY_NAME / "hello.txt"
    p.write_text("test")

    p2 = component_dir / DATA_DIRECTORY_NAME / "hello2.txt"
    p2.write_text("test")

    try:
        response = runner.invoke(step2, ["-f", component_dir / CONFIG_YAML_NAME])
        print(response.output)
        assert response.exit_code == 0
    except:
        assert False
    try:
        response = runner.invoke(step3, ["-f", component_dir / CONFIG_YAML_NAME])
        assert response.exit_code == 0
    except Exception as e:
        print(e)
        logging.error(e, exc_info=True)
        assert False

    try:
        response = runner.invoke(step4, ["-f", component_dir / CONFIG_YAML_NAME, str(p2)])
        assert response.exit_code == 0
    except:
        assert False


def test_step5(tmp_path):
    runner = CliRunner()
    os.chdir(tmp_path)
    response = runner.invoke(step1, [MODEL_NAME])
    component_dir = tmp_path / MODEL_NAME
    input_config_path = component_dir / DATA_DIRECTORY_NAME / "this_is_config_file.txt"
    input_config_path.write_text("0 0 {{parameter_1}} {{parameter_2}")

    input_data_path = component_dir / DATA_DIRECTORY_NAME / "this_is_data.txt"
    input_data_path.write_text("test")

    try:
        response = runner.invoke(step2, ["-f", component_dir / CONFIG_YAML_NAME, "-p", 2])
        assert response.exit_code == 0
    except:
        assert False
    try:
        response = runner.invoke(step3, ["-f", component_dir / CONFIG_YAML_NAME])
        assert response.exit_code == 0
    except:
        assert False

    try:
        response = runner.invoke(step4, ["-f", component_dir / CONFIG_YAML_NAME, str(input_config_path)])
        assert response.exit_code == 0
    except:
        assert False

    try:
        response = runner.invoke(step5, ["-f", component_dir / CONFIG_YAML_NAME])
        assert response.exit_code == 0
    except Exception as e:
        logging.error(e, exc_info=True)
        assert False
