import logging

import modelcatalog
from mic._utils import obtain_id
from mic.model_catalog_utils import get_api
from modelcatalog import ApiException, DatasetSpecification

RESOURCE_INPUT = "Input"
RESOURCE_OUTPUT = "Output"


class DataSpecificationCli:
    name = RESOURCE_INPUT

    def __init__(self, profile):
        self.profile = profile

    def get_one(self, _id):
        api, username = get_api(profile=self.profile)
        api_instance = modelcatalog.DatasetSpecificationApi(api)
        try:
            api_response = api_instance.datasetspecifications_id_get(id=_id, username=username)
            return api_response
        except ApiException as e:
            raise e

    def get(self):
        api, username = get_api(profile=self.profile)
        api_instance = modelcatalog.DatasetSpecificationApi(api)
        try:
            api_response = api_instance.datasetspecifications_get(username=username)
            return api_response
        except ApiException as e:
            raise e

    def post(self, request):
        api, username = get_api(profile=self.profile)
        api_instance = modelcatalog.DatasetSpecificationApi(api)
        model_configuration = DatasetSpecification(**request) if isinstance(request, dict) else request
        try:
            api_response = api_instance.datasetspecifications_post(username, dataset_specification=model_configuration)
            return api_response
        except ApiException as e:
            logging.error(
                "Exception when calling ModelConfigurationConfigurationSetupApi->modelconfigurationsetups_post: %s\n" % e)
            raise e
        return api_response

    def put(self, request):
        model_id = obtain_id(request.id)
        api, username = get_api(profile=self.profile)
        api_instance = modelcatalog.DatasetSpecificationApi(api)
        data_set = DatasetSpecification(**request) if isinstance(request, dict) else request

        try:
            # Update a Model
            return api_instance.datasetspecifications_id_put(model_id, username, dataset_specification=data_set)
        except ApiException as e:
            logging.error(
                "Exception when calling ModelConfigurationConfigurationSetupApi->modelconfigurationsetups_post: %s\n" % e)
            raise e
