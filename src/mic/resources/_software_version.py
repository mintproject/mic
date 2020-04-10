import logging
import modelcatalog
from mic._utils import first_line_new, get_api
from mic._mappings import mapping_model_configuration

from modelcatalog import ApiException
from mic.resources._modelconfiguration import ModelConfigurationCli

RESOURCE = "ModelVersion Version"


def create():
    first_line_new(RESOURCE)
    request = {}



class SoftwareVersionCli:
    name = RESOURCE
    has_configuration = {"mapping": mapping_model_configuration, "resource": ModelConfigurationCli}

    def __init__(self):
        pass

    @staticmethod
    def get():
        # create an instance of the API class
        api, username = get_api()
        api_instance = modelcatalog.SoftwareVersionApi(api)
        try:
            # List all Person entities
            api_response = api_instance.softwareversions_get(username=username)
            return api_response
        except ApiException as e:
            raise e


