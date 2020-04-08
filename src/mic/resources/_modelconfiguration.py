import logging
import modelcatalog
from mic._utils import first_line_new, get_api
from mic._mappings import *
from modelcatalog import ApiException

import click



RESOURCE = "Model Configuration"


def create(inputs=0, outputs=0, parameters=0):
    first_line_new(RESOURCE)
    request = {}


class ModelConfigurationCli:
    name = RESOURCE

    def __init__(self):
        pass

    @staticmethod
    def get():
        # create an instance of the API class
        api, username = get_api()
        api_instance = modelcatalog.ModelConfigurationApi(api)
        try:
            # List all Person entities
            api_response = api_instance.modelconfigurations_get(username=username)
            return api_response
        except ApiException as e:
            raise e

    @staticmethod
    def post(request):
        api, username = get_api()
        api_instance = modelcatalog.ModelConfigurationApi(api)
        try:
            api_response = api_instance.modelconfigurations_post(username, model=request)
        except ApiException as e:
            logging.error("Exception when calling ModelConfigurationConfigurationSetupApi->modelconfigurationsetups_post: %s\n" % e)
            raise e
        return api_response


def menu():
    first_line_new(RESOURCE)
    parameters = click.prompt('Number of parameters', type=int)
    inputs = click.prompt('Number of inputs', type=int)
    outputs = click.prompt('Number of outputs', type=int)
    return inputs, outputs, parameters