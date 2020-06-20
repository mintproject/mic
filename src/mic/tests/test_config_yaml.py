import shutil
from pathlib import Path
import os
from click.testing import CliRunner
from mic.click_encapsulate.commands import inputs, outputs, wrapper
from mic.config_yaml import get_outputs_mic, get_parameters, get_inputs_parameters, get_configs
from mic.constants import MIC_DIR, CONFIG_YAML_NAME

RESOURCES = "resources"
mic_1 = Path(__file__).parent / RESOURCES / "mic_full.yaml"
mic_empty = Path(__file__).parent / RESOURCES / "mic_empty.yaml"


def test_get_outputs():
    assert get_outputs_mic(mic_1) == {'y_csv': {'format': 'csv', 'path': 'results/y.csv'}}
    assert get_outputs_mic(mic_empty) == {}


def test_get_parameters():
    assert get_parameters(mic_1) == {'a': {'default_value': 5}, 'b': {'default_value': 4},
                                     'c': {'default_value': 6}}
    assert get_parameters(mic_empty) == {}


def test_get_configs():
    assert get_configs(mic_1) == {'config_json': {'format': 'json', 'path': 'config.json'}}
    assert get_configs(mic_empty) == {}


def test_get_inputs_parameters():
    assert get_inputs_parameters(mic_1) == ({'results_zip': {'format': 'zip', 'path': 'results.zip'},
                                             'x_csv': {'format': 'csv', 'path': 'x.csv'}},
                                            {'a': {'default_value': 5},
                                             'b': {'default_value': 4},
                                             'c': {'default_value': 6}},
                                            {'y_csv': {'format': 'csv', 'path': 'results/y.csv'}},
                                            {'config_json': {'format': 'json', 'path': 'config.json'}})
    assert get_inputs_parameters(mic_empty) == ({}, {}, {}, {})

# def test_auto_parameters():
#     os.mkdir("")

def test_issue_168(tmp_path):
    test_name = "issue_168"
    path = Path(__file__).parent / RESOURCES / test_name
    path_test_name = tmp_path / test_name
    shutil.copytree(path, path_test_name)
    runner = CliRunner()
    mic_config_arg = str(path_test_name / MIC_DIR / CONFIG_YAML_NAME)
    custom_input_1 = str(path_test_name / "DatasetSpecification.csv")
    try:
        result = runner.invoke(inputs, ["-f", mic_config_arg, custom_input_1], catch_exceptions=False)
        print(result.output)
    except Exception as e:
        print(e)
        assert False
    assert result.exit_code == 0

    result = runner.invoke(outputs, ["-f", mic_config_arg], catch_exceptions=False)
    print(result.output)
    assert result.exit_code == 0
    result = runner.invoke(wrapper, ["-f", mic_config_arg], catch_exceptions=False)
    print(result.output)

    assert result.exit_code == 0
