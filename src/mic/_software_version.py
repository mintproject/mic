import logging
import modelcatalog
from mic._model_catalog_utils import MODEL_CATALOG_URL
from mic._utils import first_line_new, get_api
from mic._mappings import mapping_model_configuration

from modelcatalog import ApiException
from mic._modelconfiguration import ModelConfigurationCli

RESOURCE = "Software Version"


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

    @staticmethod
    def put(software_version):
        api, username = get_api()
        api_instance = modelcatalog.SoftwareVersionApi(api)

        try:
            version_id = software_version.id.replace(MODEL_CATALOG_URL, '')
            api_response = api_instance.softwareversions_id_put(version_id, username,
                                                                software_version=software_version)
            return api_response
        except ApiException as e:
            logging.error(
                "Exception when calling SoftwareVersionApi->softwareversions_id_put: %s\n" % e)
            raise e
        return api_response
