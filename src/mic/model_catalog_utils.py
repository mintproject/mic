import logging

import modelcatalog
from mic.credentials import get_credentials
from modelcatalog import ApiException

MODEL_CATALOG_URL = "https://w3id.org/okn/i/mint/"


def get_label_from_response(response):
    """
    Get the response of ModelCatalog and return a list with the labels
    @param response: Response of the ModelCatalog
    @type response: List
    @return: A list with the labels
    @rtype: List
    """
    labels = []
    for resource in response:
        if isinstance(resource, dict):
            if resource["label"]:
                labels.append(resource["label"][0])
            elif resource["id"]:
                labels.append(resource["id"])
            else:
                labels.append(None)
        else:
            if resource.label:
                labels.append(resource.label[0])
            elif resource.id:
                labels.append(resource.id)
            else:
                labels.append(None)
    return labels


def create_request(values):
    """
    Create a dictionary to send the model catalog
    @param values: List with properties of the resource
    @return: dict
    """
    request = {}
    for value in values:
        request[value["id"]] = None
    return request


def get_api(profile="default"):
    try:
        credentials = get_credentials(profile)
        username = credentials[profile]["api_username"]
        password = credentials[profile]["api_password"]
    except ValueError:
        exit(1)
    configuration = login(username, password)
    return modelcatalog.ApiClient(configuration=configuration), username


def login(username, password):
    api_instance = modelcatalog.DefaultApi()
    configuration = modelcatalog.Configuration()
    try:
        api_response = api_instance.user_login_get(username, password)
        access_token = api_response["access_token"]
        configuration.access_token = access_token

    except ApiException as e:
        logging.error("Exception when calling DefaultApi->user_login_get: %s\n" % e)
        quit()
    return configuration
