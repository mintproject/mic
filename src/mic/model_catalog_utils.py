import ast
import json
import logging

import click
import modelcatalog
from mic.credentials import get_credentials
from modelcatalog import ApiException, ApiClient

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
            if hasattr(resource, "label") and resource.label:
                labels.append(resource.label[0])
            elif hasattr(resource, "id") and resource.id:
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
        username = credentials["username"]
        password = credentials["password"]
        server = credentials["server"]
    except ValueError:
        exit(1)
    except KeyError:
        click.secho("WARNING: The profile is malformed, To configure it, run:\nmic configure -p {}".format(profile),
                    fg="yellow")
        exit(1)
    configuration = _api_configuration(username, password, server)
    return ApiClient(configuration=configuration), credentials["username"]


def _api_configuration(username, password, server=None):
    configuration = modelcatalog.Configuration()
    if server is None:
        configuration.host = server
    api_instance = modelcatalog.DefaultApi(ApiClient(configuration=configuration))
    try:
        api_response = api_instance.user_login_get(username, password)
        access_token = api_response["access_token"]
        configuration.access_token = access_token

    except ApiException as e:
        logging.error("Exception when calling DefaultApi->user_login_get: %s\n" % e)
        quit()
    return configuration