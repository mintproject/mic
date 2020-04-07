import logging
import modelcatalog
from mic._utils import get_api, first_line_new
from modelcatalog import ApiException

#Version: number
RESOURCE = "Model Version"


def create():
    first_line_new(RESOURCE)
    request = {}



def push(request):
    pass
    configuration, username = get_api()
    api_instance = modelcatalog.ModelConfigurationApi(modelcatalog.ApiClient(configuration=configuration))
    try:
        api_response = api_instance.modelconfigurations_post(username, model_configuration=request)
    except ApiException as e:
        logging.error("Exception when calling ModelConfigurationSetupApi->modelconfigurationsetups_post: %s\n" % e)
        quit()
    return api_response.id
