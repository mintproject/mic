import logging

import modelcatalog
from mic.model_catalog_utils import get_api
from modelcatalog import ApiException, ModelConfiguration

RESOURCE = "Model Configuration"


class ModelConfigurationCli:
    name = RESOURCE

    def __init__(self, profile):
        self.profile = profile

    def get(self):
        api, username = get_api(profile=self.profile)
        api_instance = modelcatalog.ModelConfigurationApi(api)
        try:
            # List all Person entities
            api_response = api_instance.modelconfigurations_get(username=username)
            return api_response
        except ApiException as e:
            raise e

    def get_one(self, _id):
        api, username = get_api(profile=self.profile)
        api_instance = modelcatalog.ModelConfigurationApi(api)
        try:
            # List all Person entities
            api_response = api_instance.modelconfigurations_id_get(id=_id, username=username)
            return api_response
        except ApiException as e:
            raise e

    def post(self, request):
        api, username = get_api(profile=self.profile)
        api_instance = modelcatalog.ModelConfigurationApi(api)
        model_configuration = ModelConfiguration(**request) if isinstance(request, dict) else request
        try:
            api_response = api_instance.modelconfigurations_post(user=username, model_configuration=model_configuration)
            return api_response
        except ApiException as e:
            logging.error(
                "Exception when calling ModelConfigurationConfigurationSetupApi->modelconfigurationsetups_post: %s\n" % e)
            raise e
        return api_response
