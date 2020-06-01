import logging

import modelcatalog
from mic._mappings import mapping_dataset_specification, mapping_parameter, mapping_model_configuration
from mic._menu import call_menu_select_property
from mic.model_catalog_utils import get_api
from mic.resources.data_specification import DataSpecificationCli
from mic.resources.parameter import ParameterCli
from modelcatalog import ApiException, ModelConfiguration

RESOURCE = "Model Configuration"


def create(profile=None, request=None, parent=None):
    call_menu_select_property(mapping_model_configuration, ModelConfigurationCli(profile), request, parent=parent)


class ModelConfigurationCli:
    name = RESOURCE

    has_input = {"mapping": mapping_dataset_specification, "resource": DataSpecificationCli}
    has_output = {"mapping": mapping_dataset_specification, "resource": DataSpecificationCli}
    has_parameter = {"mapping": mapping_parameter, "resource": ParameterCli}

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

    def post(self, request):
        api, username = get_api(profile=self.profile)
        api_instance = modelcatalog.ModelConfigurationApi(api)
        model_configuration = ModelConfiguration(**request) if isinstance(request, dict) else request
        try:
            api_response = api_instance.modelconfigurations_post(username, model_configuration=model_configuration)
            return api_response
        except ApiException as e:
            logging.error(
                "Exception when calling ModelConfigurationConfigurationSetupApi->modelconfigurationsetups_post: %s\n" % e)
            raise e
        return api_response
