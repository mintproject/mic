import ast
import json
import logging

import click
import modelcatalog
from mic.credentials import get_credentials
from modelcatalog import ApiException, ApiClient, User
from mic.constants import DEFAULT_CONFIGURATION_WARNING

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
        click.secho(DEFAULT_CONFIGURATION_WARNING + " {}".format(profile), fg="yellow")
        exit(1)
    configuration = _api_configuration(username, password, profile, server)
    return ApiClient(configuration=configuration), credentials["username"]


def _api_configuration(username, password, profile, server=None):
    configuration = modelcatalog.Configuration()
    if server is not None:
        package_version = configuration.host.split('/')[-1].replace("v", '')
        configuration_version = server.split('/')[-1].replace("v", '')
        if package_version > configuration_version:
            click.secho(
                f"""WARNING: Your credentials are using Model Catalog version {configuration_version},
                but the version {package_version} is available.
                You should consider upgrading via the 'dame configure -p {profile}'""",
                fg="yellow",
            )
            click.secho("DAME is going to use the newest version", fg="yellow")
    api_instance = modelcatalog.DefaultApi(ApiClient(configuration=configuration))
    user = User(username=username, password=password)
    try:
        api_response = api_instance.user_login_post(user=user)
        access_token = ast.literal_eval(api_response)['access_token']
        configuration.access_token = access_token

    except ApiException as e:
        logging.error("Exception when calling DefaultApi->user_login_get: %s\n" % e)
        quit()
    return configuration