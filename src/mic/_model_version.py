import logging
import modelcatalog
from mic._utils import ask_simple_value, get_api_configuration, first_line_new
from modelcatalog import ApiException
import click
from mic._modelconfiguration import create as create_modelconfiguration, menu

#Version: number
mapping_model_version = {
    'Name': 'label',
    'Short Description': 'short_description',
    'Version': 'hasVersionId',
}

RESOURCE = "Model Version"


def create():
    first_line_new(RESOURCE)
    request = {}
    for key in mapping_model_version:
        value = ask_simple_value(key, RESOURCE)
        request[mapping_model_version[key]] = value
    model_configurations = []
    question_add = click.confirm('Do you want create a new configuration for the model?')
    while question_add:
        inputs, outputs, parameters = menu()
        model_configurations.append(create_modelconfiguration(parameters=parameters, inputs=inputs, outputs=outputs))
        if not click.confirm('Do you want create another configuration for the model?'):
            break
    request["hasConfiguration"] = model_configurations
    return request





def push(request):
    pass
    configuration, username = get_api_configuration()
    api_instance = modelcatalog.ModelConfigurationApi(modelcatalog.ApiClient(configuration=configuration))
    try:
        api_response = api_instance.modelconfigurations_post(username, model_configuration=request)
    except ApiException as e:
        logging.error("Exception when calling ModelConfigurationSetupApi->modelconfigurationsetups_post: %s\n" % e)
        quit()
    return api_response.id
