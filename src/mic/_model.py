import logging
import modelcatalog
from mic._utils import get_api, first_line_new, get_complex
from mic._mappings import *
from modelcatalog import ApiException, Model
import click

from mic._menu import default_menu, create_request, print_request, edit_menu, remove_menu, save_menu, push_menu, \
    add_resource

RESOURCE = "Model"


def create():
    click.clear()
    add_resource(mapping_model, RESOURCE)





def push(request):
    configuration, username = get_api()
    api_instance = modelcatalog.ModelApi(modelcatalog.ApiClient(configuration=configuration))
    try:
        api_response = api_instance.models_post(username, model=request)
    except ApiException as e:
        logging.error("Exception when calling ModelConfigurationSetupApi->modelconfigurationsetups_post: %s\n" % e)
        quit()
    print(api_response)


