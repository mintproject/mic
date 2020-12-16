from pathlib import Path

from mic.component.reprozip import generate_runner, \
    get_parameters_reprozip, get_parameter_type
from mic.config_yaml import get_spec, get_inputs, get_outputs_mic, get_parameters

RESOURCES = "resources"
DEFAULT_PATH = Path("/tmp/mint/")


# Test that mic can detect parameters from trace command
def test_param_detection():
    mic_yaml = Path("254/mic/mic.yaml")
    mic_spec = get_spec(Path(__file__).parent / RESOURCES / mic_yaml)

    repro_yaml = Path("254/.reprozip-trace/config.yml")

    repro_spec = get_spec(Path(__file__).parent / RESOURCES / repro_yaml)

    spec = get_parameters_reprozip(mic_spec, repro_spec)

    assert spec == {"step": 1,
                    "name": "test-autoparam",
                    "docker_image": "test-autoparam:latest",
                    "inputs": {"a_txt": {"path": "a.txt", "format": "txt"},
                               "in_txt": {"path": "in.txt", "format": "txt"}},
                    "code_files": {"addtoarray_sh": {"path": "addtoarray.sh", "format": "sh"}},
                    "outputs": {"out_csv": {"path": "outputs/out.csv", "format": "csv"}},
                    "parameters": {"param_1": {"name": "", "default_value": "15", "type": "int", "description": ""}}}


def test_param_detection_v2():
    mic_yaml = Path("254/mic/mic2.yaml")
    mic_spec = get_spec(Path(__file__).parent / RESOURCES / mic_yaml)

    repro_yaml = Path("254/.reprozip-trace2/config.yml")

    repro_spec = get_spec(Path(__file__).parent / RESOURCES / repro_yaml)

    spec = get_parameters_reprozip(mic_spec, repro_spec)

    assert spec == {"step": 1,
                    "name": "parameter-test",
                    "docker_image": "parameter-test:latest",
                    "inputs": {"a_txt": {"path": "a.txt", "format": "txt"},
                               "in_txt": {"path": "in.txt", "format": "txt"}},
                    "code_files": {"addtoarray_sh": {"path": "addtoarray.sh", "format": "sh"}},
                    "outputs": {"out_csv": {"path": "outputs/out.csv", "format": "csv"}},
                    "parameters": {
                        "param_1": {"name": "", "default_value": "15", "type": "int", "description": ""},
                        "param_2": {"name": "", "default_value": "hello", "type": "str", "description": ""},
                        "param_3": {"name": "", "default_value": "-3.1415", "type": "float", "description": ""},
                        "param_4": {"name": "", "default_value": "-15", "type": "int", "description": ""},
                        "param_5": {"name": "", "default_value": "string-special", "type": "str", "description": ""}
                    }
                    }

def test_wrapper_code():
    mic_yaml = Path("254/mic/mic3.yaml")
    repro_yaml = Path("254/.reprozip-trace2/config.yml")

    repro_spec = get_spec(Path(__file__).parent / RESOURCES / repro_yaml)

    inp = get_inputs(Path(__file__).parent / RESOURCES / mic_yaml)
    outp = get_outputs_mic(Path(__file__).parent / RESOURCES / mic_yaml)
    params = get_parameters(Path(__file__).parent / RESOURCES / mic_yaml)

    code = generate_runner(repro_spec, DEFAULT_PATH, inp, outp, params)
    assert code == "\npushd .\n/bin/sh ./addtoarray.sh ${a_txt} ${in_txt} ${param_1} \"${param_2}\" ${param_3} " \
                   "${param_4} \"${param_5}\" \"${param_6}\"\npopd"



# General test cases to make sure mic auto param can guess the parameter's type from the command line
def test_get_parameter_type():
    assert get_parameter_type("15") == "int"
    assert get_parameter_type("-1243432") == "int"
    assert get_parameter_type("22.43566457") == "float"
    assert get_parameter_type("-9574322.4667853") == "float"
    assert get_parameter_type("0") == "int"
    assert get_parameter_type("-0") == "int"
    assert get_parameter_type("-0.0") == "float"
    assert get_parameter_type("0.0") == "float"
    assert get_parameter_type("this is a long string parameter") == "str"
    assert get_parameter_type("[1,2,3,4,5,6]") == "str"
    assert get_parameter_type("--") == "str"
    assert get_parameter_type(".") == "char"
    assert get_parameter_type("c") == "char"
    assert get_parameter_type("TRUE") == "bool"
    assert get_parameter_type("-false") == "str"



# def test_get_inputs_aggregate_false():
#     """
#     We're testing the reprozip keys: inputs_outputs and other_files using aggregate false
#     """
#     swat_inputs_v1 = swat_inputs.copy()
#     swat_inputs_v1.append("/tmp/mint/example.txt")
#     yml = "swat_test_v2.yml"
#     spec = get_spec(Path(__file__).parent / RESOURCES / yml)
#     inputs = get_inputs_outputs_reprozip(spec, DEFAULT_PATH, aggregrate=False)
#     assert sorted(swat_inputs_v1) == sorted(inputs)
#
#
# def test_get_inputs_aggregate_true():
#     swat_inputs_v1 = swat_inputs.copy()
#     swat_inputs_v1.append("/tmp/mint/example.txt")
#     yml = "swat_test_v2.yml"
#     spec = get_spec(Path(__file__).parent / RESOURCES / yml)
#     inputs = get_inputs_outputs_reprozip(spec, DEFAULT_PATH, aggregrate=True)
#     assert ["/tmp/mint/TxtInOut", "/tmp/mint/example.txt"] == sorted(inputs)
#
#
# def test_generate_runner():
#     yml = "swat_test.yml"
#     spec = get_spec(Path(__file__).parent / RESOURCES / yml)
#     result = generate_runner(spec, DEFAULT_PATH, {}, {}, {})
#     expected = """
# pushd TxtInOut
# ./swat670
# popd
# pushd TxtInOut
# ./swat670
# popd"""
#     assert expected == result
#
#
# def test_generate_runner_v1():
#     yml = "swat_test_v2.yml"
#     spec = get_spec(Path(__file__).parent / RESOURCES / yml)
#     result = generate_runner(spec, DEFAULT_PATH, {}, {}, {})
#     expected = """
# pushd TxtInOut
# ./swat670
# popd
# pushd TxtInOut
# ./swat670 -p 1
# popd"""
#     assert expected == result
#
#
# def test_generate_pre_runner_1():
#     yml = "mic_full.yaml"
#     spec = get_spec(Path(__file__).parent / RESOURCES / yml)
#     assert generate_pre_runner(spec, DEFAULT_PATH) == ""
#
#
# def test_generate_pre_runner_2():
#     yml = "mic_2.yaml"
#     spec = get_spec(Path(__file__).parent / RESOURCES / yml)
#     assert generate_pre_runner(spec, DEFAULT_PATH) == ""
#
#
# def test_generate_pre_runner_3():
#     yml = "mic_3.yaml"
#     spec = get_spec(Path(__file__).parent / RESOURCES / yml)
#     assert generate_pre_runner(spec, DEFAULT_PATH) == "\ncp -rv x.csv results/x.csv"
