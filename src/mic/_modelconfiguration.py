import logging
import modelcatalog
from mic._dataspecification import add_input, add_output
from mic._parameter import add_parameter
from mic._utils import ask_simple_value, get_api_configuration, first_line_new
from modelcatalog import ApiException

import click

mapping_model_configuration = {
    'Name': 'label',
}

RESOURCE = "Model Configuration"


def create(inputs=0, outputs=0, parameters=0):
    first_line_new(RESOURCE)
    request = {}
    for key in mapping_model_configuration:
        value = ask_simple_value(key, RESOURCE)
        request[mapping_model_configuration[key]] = value

    parameters_list = []
    outputs_list = []
    inputs_list = []
    for i in range(0, parameters):
        parameters_list.append(add_parameter(i))
    for i in range(0, inputs):
        inputs_list.append(add_input(i))
    for i in range(0, outputs):
        outputs_list.append(add_output(i))

    request["hasInput"] = inputs_list
    request["hasOutput"] = outputs_list
    request["hasParameter"] = parameters_list
    return request


def push(request):
    configuration, username = get_api_configuration()
    api_instance = modelcatalog.ModelConfigurationApi(modelcatalog.ApiClient(configuration=configuration))
    try:
        api_response = api_instance.modelconfigurations_post(username, model_configuration=request)
    except ApiException as e:
        logging.error("Exception when calling ModelConfigurationSetupApi->modelconfigurationsetups_post: %s\n" % e)
        quit()
    return api_response.id

def menu():
    first_line_new(RESOURCE)
    parameters = click.prompt('Number of parameters', type=int)
    inputs = click.prompt('Number of inputs', type=int)
    outputs = click.prompt('Number of outputs', type=int)
    return inputs, outputs, parameters