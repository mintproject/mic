import uuid
from pathlib import Path

import click
import validators
from dame.cli_methods import create_sample_resource
from mic._menu import parse
from mic._utils import obtain_id
from mic.config_yaml import get_inputs_parameters, get_key_spec, DOCKER_KEY
from mic.constants import TYPE_PARAMETER, TYPE_DATASET, TYPE_SOFTWARE_IMAGE, MINT_COMPONENT_KEY, \
    TYPE_MODEL_CONFIGURATION, TYPE_SOFTWARE_VERSION, MINT_INSTANCE, FORMAT_KEY, PATH_KEY, \
    TYPE_DATA_TRANSFORMATION, MAP_PYTHON_MODEL_CATALOG
from mic.drawer import print_choices
from mic.model_catalog_utils import get_label_from_response
from mic.resources.data_specification import DataSpecificationCli
from mic.resources.data_transformation import DataTransformationCli
from mic.resources.model import ModelCli
from mic.resources.model_configuration import ModelConfigurationCli
from mic.resources.software_version import SoftwareVersionCli
from modelcatalog import DatasetSpecification, ModelConfiguration, SoftwareImage, Parameter, Model, SoftwareVersion, \
    DataTransformation


def generate_uuid():
    return "https://w3id.org/okn/i/mint/{}".format(str(uuid.uuid4()))


def create_model_catalog_resource(mint_config_file, name=None, execution_dir=None, allow_local_path=True):
    name = name if name else mint_config_file.parent.name
    inputs, parameters, outputs, configs = get_inputs_parameters(mint_config_file)

    model_catalog_inputs = create_data_set_resource(allow_local_path, inputs,
                                                    execution_dir) if inputs else None
    model_catalog_outputs = create_data_set_resource(False, outputs,
                                                     mint_config_file.parent) if outputs else None
    model_catalog_parameters = create_parameter_resource(parameters)

    image = get_key_spec(mint_config_file, DOCKER_KEY)
    code = get_key_spec(mint_config_file, MINT_COMPONENT_KEY)
    model_configuration = ModelConfiguration(type=[TYPE_MODEL_CONFIGURATION],
                                             label=[str(name)],
                                             has_input=model_catalog_inputs,
                                             has_output=model_catalog_outputs,
                                             has_parameter=model_catalog_parameters,
                                             )
    if allow_local_path:
        return model_configuration

    if image is None:
        click.secho("Upload Failed. Missing information DockerImage", fg='red')
    else:
        software_image = SoftwareImage(id=generate_uuid(), label=[image], type=[TYPE_SOFTWARE_IMAGE])
        model_configuration.has_software_image = [software_image]

    if code is None:
        click.secho("Failed to upload. Missing information zip file", fg="red")
    else:
        model_configuration.has_component_location = [code]
    return model_configuration


def create_parameter_resource(parameters):
    model_catalog_parameters = []
    position = 1
    for key, item in parameters.items():
        data_type = "string"
        if "type" in item and item["type"] != '' and item["type"] is not None:
            data_type = MAP_PYTHON_MODEL_CATALOG[item["type"]]
        _parameter = Parameter(id=generate_uuid(), label=[key], position=[position], type=[TYPE_PARAMETER], has_data_type=[data_type])
        _parameter.has_default_value = [item["default_value"]]
        model_catalog_parameters.append(_parameter)
        position += 1
    if not model_catalog_parameters:
        return []
    return model_catalog_parameters


def create_data_set_resource(allow_local_path, inputs, execution_dir):
    model_catalog_inputs = []
    position = 1
    for key, item in inputs.items():
        _format = item[FORMAT_KEY] if FORMAT_KEY in item else "unknown"
        _input = DatasetSpecification(id=generate_uuid(), label=[key], has_format=[_format], position=[position], type=[TYPE_DATASET])
        if allow_local_path:
            p = Path(execution_dir) / item[PATH_KEY]
            create_sample_resource(_input, str(p))
        model_catalog_inputs.append(_input)
        position += 1
    if not model_catalog_inputs:
        return []
    return model_catalog_inputs


def publish_model_configuration(model_configuration, profile):
    model_configuration_cli = ModelConfigurationCli(profile=profile)
    api_response_mc = model_configuration_cli.post(model_configuration)

    if not validators.url(api_response_mc.id):
        api_response_mc.id = "{}{}".format(MINT_INSTANCE, api_response_mc.id)
    click.echo("A model component must be associated with a model")
    model_cli = ModelCli(profile=profile)
    models = model_cli.get()
    labels = get_show_models(models, "models")
    if click.confirm("Do you want to use an existing model?", default=True):
        api_response, model_id, software_version_id = handle_existing_model(profile, api_response_mc, labels, model_cli)
    else:
        api_response = create_new_model(model_cli, api_response_mc)
        software_version_id = api_response.has_version[0].id
        model_id = api_response.id
    click.secho("Your Model Component has been uploaded", fg="green")
    return api_response, api_response_mc, model_id, software_version_id


def handle_existing_model(profile, api_response_mc, labels, model_cli):
    models = model_cli.get()
    choice = click.prompt("Please select the model to use",
                          default=1,
                          show_choices=False,
                          type=click.Choice(list(range(1, len(labels) + 1))),
                          value_proc=parse
                          )
    selected_model = models[choice - 1]
    software_version_cli = SoftwareVersionCli(profile)

    labels = get_show_models_version(selected_model.has_version, software_version_cli)
    software_version = handle_new_existing_software_version(labels, api_response_mc, selected_model,
                                                            software_version_cli)

    if selected_model.has_version:
        selected_model.has_version.append(software_version)
    else:
        selected_model.has_version = [software_version]
    return model_cli.put(selected_model), selected_model.id, software_version.id


def handle_new_existing_software_version(labels, api_response_mc, selected_model, software_version_cli):
    if click.confirm("Do you want to use an existing version?", default=True):
        choice = click.prompt("Select enter the number of version to use",
                              default=1,
                              show_choices=False,
                              type=click.Choice(list(range(1, len(labels) + 1))),
                              value_proc=parse
                              )
        model_version = selected_model.has_version[choice - 1]
        model_version = software_version_cli.get_one(obtain_id(model_version.id))
        if model_version.has_configuration:
            model_version.has_configuration.append(api_response_mc)
        else:
            model_version.has_configuration = [api_response_mc]
        return software_version_cli.put(model_version)
    else:
        click.echo("Please, enter the information about the new version")
        _version = click.prompt("Version of the model")
        description = click.prompt("A short description of the version")
        software_version = SoftwareVersion(label=[_version],
                                           description=[description],
                                           type=[TYPE_SOFTWARE_VERSION],
                                           has_version_id=[_version],
                                           has_configuration=[api_response_mc])
        return software_version_cli.post(software_version)


def create_new_model(model_cli, model_configuration):
    click.echo("Please enter the information about the Model")
    name = click.prompt("Name of the model")
    model_description = click.prompt("A short description of the Model")
    _version = click.prompt("Version of the model")
    version_description = click.prompt("A short description of the version")
    new_model = Model(label=[name],
                      has_version=[SoftwareVersion(label=[_version],
                                                   description=[version_description],
                                                   type=[TYPE_SOFTWARE_VERSION],
                                                   has_version_id=[_version],
                                                   has_configuration=[model_configuration])
                                   ],
                      description=[model_description])
    return model_cli.post(new_model)


def get_show_models_version(resources, software_version_cli):
    labels = get_label_from_response([software_version_cli.get_one(obtain_id(i.id)) for i in resources])
    click.secho("Existing versions are:")
    print_choices(labels)
    return labels


def get_show_models(resources, resource_name):
    labels = get_label_from_response(resources)
    click.secho("Existing {} are:".format(resource_name))
    print_choices(labels)
    return labels


def publish_data_transformation(data_transformation, profile):
    data_transformation_cli = DataTransformationCli(profile=profile)
    api_response_mc = data_transformation_cli.post(data_transformation)
    if not validators.url(api_response_mc.id):
        api_response_mc.id = "{}{}".format(MINT_INSTANCE, api_response_mc.id)
    click.echo("A DataTransformation can be associated with a ModelConfiguration")
    if click.confirm("Do you want to skip it?", default=False, show_default=True):
        return api_response_mc
    
    model_configuration_cli = ModelConfigurationCli(profile=profile)

    model_configurations = model_configuration_cli.get()
    labels = get_show_models(model_configurations, "Model Configurations")

    choice = click.prompt("Select enter the number of Model Configuration to use",
                          default=1,
                          show_choices=False,
                          type=click.Choice(list(range(1, len(labels) + 1))),
                          value_proc=parse
                          )
    model_configuration = model_configuration_cli.get_one(obtain_id(model_configurations[choice - 1].id))

    labels = get_show_models(model_configuration.has_input, "Inputs")
    choice = click.prompt("Select enter the number of inputs to use",
                          default=1,
                          show_choices=False,
                          type=click.Choice(list(range(1, len(labels) + 1))),
                          value_proc=parse
                          )

    dataset_cli = DataSpecificationCli(profile=profile)
    _input = dataset_cli.get_one(obtain_id(model_configuration.has_input[choice - 1].id))

    if _input.has_data_transformation:
        _input.has_data_transformation.append(api_response_mc)
    else:
        _input.has_data_transformation = [api_response_mc]
    dataset_cli.put(_input)
    click.secho("Your Data Transformation has been published", fg="green")
    return api_response_mc


def create_data_transformation_resource(mint_config_file, name=None, execution_dir=None, allow_local_path=True):
    name = name if name else mint_config_file.parent.name
    inputs, parameters, outputs, configs = get_inputs_parameters(mint_config_file)

    model_catalog_inputs = create_data_set_resource(allow_local_path, inputs,
                                                    execution_dir) if inputs else None
    model_catalog_outputs = create_data_set_resource(False, outputs,
                                                     mint_config_file.parent) if outputs else None
    model_catalog_parameters = create_parameter_resource(parameters)

    image = get_key_spec(mint_config_file, DOCKER_KEY)
    code = get_key_spec(mint_config_file, MINT_COMPONENT_KEY)
    data_transformation = DataTransformation(type=[TYPE_DATA_TRANSFORMATION],
                                             label=[str(name)],
                                             has_input=model_catalog_inputs,
                                             has_output=model_catalog_outputs,
                                             has_parameter=model_catalog_parameters,
                                             )
    if allow_local_path:
        return data_transformation

    if image is None:
        click.secho("Failed to publish. Missing information DockerImage")
    else:
        software_image = SoftwareImage(id=generate_uuid(), label=[image], type=[TYPE_SOFTWARE_IMAGE])
        data_transformation.has_software_image = [software_image]

    if code is None:
        click.secho("Failed to publish. Missing information zip file")
    else:
        data_transformation.has_component_location = [code]
    return data_transformation
