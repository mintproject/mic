import logging
import modelcatalog
from mic._utils import get_api
from mic._mappings import mapping_person, mapping_model, mapping_software_version, mapping_image
from modelcatalog import ApiException, Model
import click

from mic._menu import call_menu_select_property
from mic._person import PersonCli
from mic._image import ImageCli
from mic._software_version import SoftwareVersionCli

RESOURCE = "Model"


def create(request=None):
    click.clear()
    call_menu_select_property(mapping_model, ModelCli(), request)


class ModelCli:
    name = RESOURCE

    author = {"mapping": mapping_person, "resource": PersonCli}
    contributor = {"mapping": mapping_person, "resource": PersonCli}
    has_version = {"mapping": mapping_software_version, "resource": SoftwareVersionCli}
    has_contact_person = {"mapping": mapping_person, "resource": PersonCli}

    author = {"mapping": mapping_person, "resource": PersonCli}
    contributor = {"mapping": mapping_person, "resource": PersonCli}
    has_version = {"mapping": mapping_software_version, "resource": SoftwareVersionCli}
    has_contact_person = {"mapping": mapping_person, "resource": PersonCli}
    logo = {"mapping": mapping_image, "resource": ImageCli}

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
        model = Model(**request)
        try:
            api_response = api_instance.models_post(username, model=model)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ModelConfigurationSetupApi->modelconfigurationsetups_post: %s\n" % e)
            raise e