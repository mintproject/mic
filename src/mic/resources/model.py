import logging
import modelcatalog
from dame.utils import obtain_id
from mic._mappings import mapping_person, mapping_model, mapping_software_version, mapping_image
from modelcatalog import ApiException, Model
import click

from mic._menu import call_menu_select_property
from mic.resources.person import PersonCli
from mic.resources.image import ImageCli
from mic.resources.software_version import SoftwareVersionCli

from mic.model_catalog_utils import get_api

RESOURCE = "Model"


def create(profile=None, request=None):
    click.clear()
    call_menu_select_property(mapping_model, ModelCli(profile), request)


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

    def __init__(self, profile):
        self.profile = profile


    def get(self):
        # create an instance of the API class
        api, username = get_api(profile=self.profile)
        api_instance = modelcatalog.ModelApi(api_client=api)
        try:
            # List all Person entities
            api_response = api_instance.models_get(username=username)
            return api_response
        except ApiException as e:
            raise e

    def post(self, request):
        api, username = get_api(profile=self.profile)
        api_instance = modelcatalog.ModelApi(api)
        model = Model(**request) if isinstance(request, dict) else request
        try:
            api_response = api_instance.models_post(username, model=model)
            return api_response
        except ApiException as e:
            logging.error("Exception when calling ModelConfigurationSetupApi->modelconfigurationsetups_post: %s\n" % e)
            raise e

    def put(self, request):
        model_id = obtain_id(request.id)
        api, username = get_api(profile=self.profile)
        api_instance = modelcatalog.ModelApi(api)
        model = Model(**request) if isinstance(request, dict) else request

        try:
            # Update a Model
            return api_instance.models_id_put(model_id, username, model=model)
        except ApiException as e:
            print("Exception when calling ModelApi->models_id_put: %s\n" % e)