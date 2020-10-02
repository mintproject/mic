from typing import Dict

parameter_list = ["int", "boolean", "string"]
input_list = ["File"]


def is_parameters(_type: str):
    _exit = True if _type in parameter_list else False
    return _exit


def is_input(_type: str):
    _exit = True if _type in input_list else False
    return _exit


def get_parameters(spec: Dict):
    parameters = []
    for key, item in spec["inputs"].items():
        if "type" in item and item["type"]:
            parameters.append(item)
    return parameters


def get_inputs(spec: Dict):
    parameters = []
    for key, item in spec["inputs"].items():
        if "type" in item and item["type"]:
            parameters.append(item)
    return parameters
