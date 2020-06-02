# -*- coding: utf-8 -*-

import logging

from jsonschema import Draft7Validator


schemaVersion = "0.0.1"

schema = {
    "type": "object",
    "required": ["inputs", "parameters", "outputs"],
    "properties": {
        "schemaVersion": {"type": "string"},
        "inputs": {"type": "object", "$ref": "#/definitions/data_file"},
        "outputs": {"type": "object", "$ref": "#/definitions/data_file"},
        "parameters": {"type": "object", "$ref": "#/definitions/parameters"},
    },

    "definitions": {
        "data_file": {
            "type": ["object"],
            "required": ["name", "path"],
            "properties": {
                "name": {"type": "string"},
                "path": {"type": "string"},
            },
        },
        "parameters": {
            "type": ["object"],
            "required": ["name", "default_value"],
            "properties": {
                "name": {"type": "string"},
                "default_value": {"type": ["string", "number", "bool"]},
            },
        },
    },

}
# Missing extension for variables of each input and variable of each output

v = Draft7Validator(schema)


def get_schema():
    return schema


def get_schema_version():
    return schemaVersion


def _msg(e):
    """Generate a user friendly error message."""
    return e.message


def check_package_spec(spec):
    """Check package specification."""
    err = []
    for e in v.iter_errors(spec):
        err.append(_msg(e))
        logging.error(_msg(e))

    if err:
        raise ValueError("Invalid component specification.")
