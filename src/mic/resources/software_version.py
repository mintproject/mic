import logging
import modelcatalog
from mic.model_catalog_utils import MODEL_CATALOG_URL
from mic._utils import first_line_new
from mic.model_catalog_utils import get_api
from mic._mappings import mapping_model_configuration

from modelcatalog import ApiException, SoftwareVersion
from mic.resources.model_configuration import ModelConfigurationCli

RESOURCE = "Software Version"


def create():
    first_line_new(RESOURCE)
    request = {}


class SoftwareVersionCli:
    name = RESOURCE
    has_configuration = {"mapping": mapping_model_configuration, "resource": ModelConfigurationCli}

    def __init__(self, profile=None):
        self.profile = profile

    def get_one(self, _id):
        api, username = get_api(profile=self.profile)
        api_instance = modelcatalog.SoftwareVersionApi(api)
        try:
            # List all Person entities
            print(_id)
            api_response = api_instance.softwareversions_id_get(id=_id, username=username)
            return api_response
        except ApiException as e:
            raise e


    def get(self):
        api, username = get_api(profile=self.profile)
        api_instance = modelcatalog.SoftwareVersionApi(api)
        try:
            # List all Person entities
            api_response = api_instance.softwareversions_get(username=username)
            return api_response
        except ApiException as e:
            raise e

    def put(self, software_version):
        api, username = get_api(profile=self.profile)
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

    def post(self, request):
        api, username = get_api(profile=self.profile)
        api_instance = modelcatalog.SoftwareVersionApi(api)
        software_version = SoftwareVersion(**request) if isinstance(request, dict) else request
        try:
            api_response = api_instance.softwareversions_post(username, software_version=software_version)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ModelConfigurationSetupApi->modelconfigurationsetups_post: %s\n" % e)
            raise