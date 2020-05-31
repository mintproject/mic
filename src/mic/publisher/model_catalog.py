import uuid
from pathlib import Path

import click
from dame.cli_methods import create_sample_resource
from mic._menu import parse
from mic.config_yaml import get_inputs_parameters, get_key_spec, DOCKER_KEY
from mic.constants import TYPE_PARAMETER, TYPE_DATASET, TYPE_SOFTWARE_IMAGE, MINT_COMPONENT_KEY, \
    TYPE_MODEL_CONFIGURATION
from mic.drawer import print_choices
from mic.model_catalog_utils import get_label_from_response
from mic.resources.model import ModelCli
from modelcatalog import DatasetSpecification, ModelConfiguration, SoftwareImage, Parameter, Model, SoftwareVersion


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
    position = 1
    response = []
    if outputs:
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
    response = response if response else None
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


def publish_model_configuration(model_configuration, profile):
    api_response = create_new_model(profile, model_configuration)
    # if click.confirm("Do you want to create new one?", default=True):
    #    api_response = create_new_model(model_cli, model_configuration)
    # else:
    #    api_response = select_existing_resource(labels, model_cli, model_configuration, models)
    click.secho("Your Model Component has been published", fg="green")
    return api_response


def handle_model(profile, model_configuration):
    model_cli = ModelCli(profile=profile)
    models = model_cli.get()
    labels = get_show_models(models, "models")
    choice = click.prompt("Please select the model to use",
                          default=1,
                          show_choices=False,
                          type=click.Choice(list(range(1, len(labels) + 1))),
                          value_proc=parse
                          )
    selected_model = models[choice - 1]
    software_versions = selected_model.has_version
    labels = get_show_models(software_versions, "version")
    handle_model_version(labels, model_configuration, selected_model)
    return model_cli.put(selected_model)


def handle_model_version(labels, model_configuration, selected_model):
    if not click.confirm("Do you want to use an existing version?", default=True):
        choice = click.prompt("Select the resource to edit",
                              default=1,
                              show_choices=False,
                              type=click.Choice(list(range(1, len(labels) + 1))),
                              value_proc=parse
                              )
        existing_configurations = selected_model.has_version[choice - 1].has_configuration
        if existing_configurations:
            existing_configurations.append(model_configuration)
        else:
            existing_configurations = [model_configuration]

    else:
        click.echo("Please, enter the information about the new version")
        _version = click.prompt("Version of the model")
        software_version = SoftwareVersion(label=[_version],
                                           type=[TYPE_SOFTWARE_IMAGE],
                                           has_version_id=[_version],
                                           has_configuration=[model_configuration])
        if selected_model.has_version:
            selected_model.has_version.append(software_version)
        else:
            selected_model.has_version = [software_version]


def create_new_model(model_cli, model_configuration):
    click.echo("Please enter the information about the Model")
    name = click.prompt("Name of the model")
    _version = click.prompt("Version of the model")
    new_model = Model(label=[name],
                      has_version=[SoftwareVersion(label=[_version], has_version_id=[_version],
                                                   has_configuration=[model_configuration])])
    return model_cli.post(new_model)


def get_show_models(resources, resource_name):
    labels = get_label_from_response(resources)
    print_choices(labels)
    click.secho("Existing {} are:".format(resource_name))
    print_choices(labels)
    return labels
