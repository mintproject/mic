import logging
import modelcatalog
from mic._utils import first_line_new, get_api_configuration
from modelcatalog import ApiException

import click



RESOURCE = "Model Configuration"


def create(inputs=0, outputs=0, parameters=0):
    first_line_new(RESOURCE)
    request = {}


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