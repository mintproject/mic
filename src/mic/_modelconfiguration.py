import logging
import modelcatalog
from mic._menu import call_menu_select_property
from mic._mappings import mapping_dataset_specification, mapping_parameter, mapping_model_configuration
from mic._utils import get_api
from modelcatalog import ApiException, ModelConfiguration

from mic._dataspecification import DataSpecificationCli
from mic._parameter import ParameterCli

RESOURCE = "Model Configuration"


def create(request=None, parent=None):
    call_menu_select_property(mapping_model_configuration, ModelConfigurationCli(), request, parent=parent)


class ModelConfigurationCli:
    name = RESOURCE

    has_input = {"mapping": mapping_dataset_specification, "resource": DataSpecificationCli}
    has_output = {"mapping": mapping_dataset_specification, "resource": DataSpecificationCli}
    has_parameter = {"mapping": mapping_parameter, "resource": ParameterCli}

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
        model_configuration = ModelConfiguration(**request)

        try:
            api_response = api_instance.modelconfigurations_post(username, model_configuration=model_configuration)
            return api_response
        except ApiException as e:
            logging.error(
                "Exception when calling ModelConfigurationConfigurationSetupApi->modelconfigurationsetups_post: %s\n" % e)
            raise e
        return api_response
