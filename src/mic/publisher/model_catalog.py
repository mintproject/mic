import uuid
from pathlib import Path

import click
from mic.constants import TYPE_PARAMETER, TYPE_DATASET, TYPE_SOFTWARE_IMAGE, MINT_COMPONENT_KEY, \
    TYPE_MODEL_CONFIGURATION
from dame.cli_methods import create_sample_resource
from mic.config_yaml import get_inputs_parameters, get_key_spec, DOCKER_KEY, MINT_COMPONENT_ZIP
from modelcatalog import DatasetSpecification, ModelConfiguration, SoftwareImage, Parameter


def generate_uuid():
    return "https://w3id.org/okn/i/mint/{}".format(str(uuid.uuid4()))


def create_model_catalog_resource(mint_config_file, allow_local_path=True):
    name = mint_config_file.parent.name
    inputs, parameters, outputs, configs = get_inputs_parameters(mint_config_file)

    model_catalog_inputs = create_input_resource(allow_local_path, inputs, name)
    model_catalog_outputs = create_output_resource(allow_local_path, outputs, name)
    model_catalog_parameters = create_parameter_resource(parameters)

    image = get_key_spec(mint_config_file, DOCKER_KEY)
    code = get_key_spec(mint_config_file, MINT_COMPONENT_KEY)

    model_configuration = ModelConfiguration(id=generate_uuid(),
                                             type=[TYPE_MODEL_CONFIGURATION],
                                             label=[str(name)],
                                             has_input=model_catalog_inputs,
                                             has_output=model_catalog_outputs,
                                             has_parameter=model_catalog_parameters,
                                             )
    if allow_local_path:
        return model_configuration

    if image is None:
        click.secho("Failed to publish. Missing information DockerImage")
    else:
        software_image = SoftwareImage(label=[image], type=[TYPE_SOFTWARE_IMAGE])
        model_configuration.has_software_image = [software_image]

    if code is None:
        click.secho("Failed to publish. Missing information zip file")
    else:
        model_configuration.has_component_location = [code]
    return model_configuration


def create_parameter_resource(parameters):
    model_catalog_parameters = []
    position = 1
    for key, item in parameters.items():
        _parameter = Parameter(id=generate_uuid(), label=[key], position=[position], type=[TYPE_PARAMETER])
        _parameter.has_default_value = [item["default_value"]]
        model_catalog_parameters.append(_parameter)
        position += 1
    if not model_catalog_parameters:
        return None
    return model_catalog_parameters


def create_output_resource(allow_local_path, outputs, name):
    response = []
    position = 1
    if outputs:
        response = None
        for key, item in outputs.items():
            try:
                _format = item["path"].split('.')[-1]
            except:
                _format = "unknown"
            _input = DatasetSpecification(label=[key], has_format=[_format], position=[position], type=[TYPE_DATASET])
            if allow_local_path:
                p = Path(name) / item["path"]
                create_sample_resource(_input, str(p.resolve()))
            response.append(_input)
            position += 1
    else:
        response = None
    return response


def create_input_resource(allow_local_path, inputs, name):
    model_catalog_inputs = []
    position = 1
    for key, item in inputs.items():
        try:
            if Path(item["path"]).is_dir():
                _format = "zip"
            else:
                _format = item["path"].name.split('.')[-1]
        except:
            _format = "unknown"
        _input = DatasetSpecification(label=[key], has_format=[_format], position=[position], type=[TYPE_DATASET])
        if allow_local_path:
            p = Path(name) / item["path"]
            create_sample_resource(_input, str(p.resolve()))
        model_catalog_inputs.append(_input)
        position += 1

    if not model_catalog_inputs:
        return None
    return model_catalog_inputs
