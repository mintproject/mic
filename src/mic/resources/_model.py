import logging
import modelcatalog
from mic._model_catalog_utils import MODEL_CATALOG_URL
from mic._utils import get_api
from mic._mappings import *
from modelcatalog import ApiException
import click

from mic._menu import call_menu_select_property

RESOURCE = "Model"


def create(request=None):
    click.clear()
    call_menu_select_property(mapping_model, ModelCli(), request)


class ModelCli:
    name = RESOURCE
    url = MODEL_CATALOG_URL

    def __init__(self):
        pass

    @staticmethod
    def get():
        # create an instance of the API class
        api, username = get_api()
        api_instance = modelcatalog.ModelApi(api_client=api)
        try:
            # List all Person entities
            api_response = api_instance.models_get(username=username)
            return api_response
        except ApiException as e:
            raise e

    def post(self, request):
        api, username = get_api()
        api_instance = modelcatalog.ModelApi(api)
        try:
            api_response = api_instance.models_post(username, model=request)
            self.url = "{}{}".format(self.url, api_response.id)
        except ApiException as e:
            logging.error("Exception when calling ModelConfigurationSetupApi->modelconfigurationsetups_post: %s\n" % e)
            raise e
