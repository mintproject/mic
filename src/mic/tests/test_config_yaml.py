from pathlib import Path

from mic.config_yaml import get_outputs, get_parameters, get_inputs_parameters, get_configs

RESOURCES = "resources"
mic_1 = Path(__file__).parent / RESOURCES / "mic_full.yaml"
mic_empty = Path(__file__).parent / RESOURCES / "mic_empty.yaml"


def test_get_outputs():
    assert get_outputs(mic_1) == {'y_csv': {'format': 'csv', 'path': 'results/y.csv'}}
    assert get_outputs(mic_empty) == {}


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
    assert get_inputs_parameters(mic_empty) == ({},{},{},{})
