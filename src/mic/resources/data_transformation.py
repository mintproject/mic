import logging

import modelcatalog
from mic.model_catalog_utils import get_api
from modelcatalog import ApiException, DataTransformation

RESOURCE = "Data Transformation"


class DataTransformationCli:
    name = RESOURCE

    def __init__(self, profile):
        self.profile = profile

    def get(self):
        api, username = get_api(profile=self.profile)
        api_instance = modelcatalog.DataTransformationApi(api)
        try:
            # List all Person entities
            api_response = api_instance.datatransformations_get(username=username)
            return api_response
        except ApiException as e:
            raise e

    def post(self, request):
        api, username = get_api(profile=self.profile)
        api_instance = modelcatalog.DataTransformationApi(api)
        data_transformation = DataTransformation(**request) if isinstance(request, dict) else request
        try:
            api_response = api_instance.datatransformations_post(username, data_transformation=data_transformation)
            return api_response
        except ApiException as e:
            logging.error(
                "Exception when calling ModelConfigurationConfigurationSetupApi->modelconfigurationsetups_post: %s\n" % e)
            raise e
        return api_response
