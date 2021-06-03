import ast
import json
import logging
import validators
from modelcatalog import ApiException, SampleResource
import uuid
import click
import modelcatalog
from mic.credentials import get_credentials
from modelcatalog import ApiException, ApiClient, User
from mic.constants import DEFAULT_CONFIGURATION_WARNING

MODEL_CATALOG_URL = "https://w3id.org/okn/i/mint/"
KEYS_REQUIRED_PARAMETER = {"has_default_value", "position"}
KEYS_REQUIRED_OUTPUT = {"label", "has_format", "position"}
KEYS_REQUIRED_INPUT = {"has_fixed_resource"}

def convert_object_to_dict(o):
    if isinstance(o, object):
        return o.to_dict()
    return o


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
    configuration = _api_configuration(username, password, server)
    return ApiClient(configuration=configuration), credentials["username"]


def _api_configuration(username, password, server=None):
    configuration = modelcatalog.Configuration()
    if server:
        configuration.host = server
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

def obtain_id(url):
    if validators.url(url):
        return url.split('/')[-1]
    return url

def build_output(outputs):
    line = ""
    for _output in outputs:
        _output = convert_object_to_dict(_output)
        if not _output.keys() >= KEYS_REQUIRED_OUTPUT:
            raise ValueError(f'{_output["id"]}  has not the required information')
        label = _output["label"][0]
        extension = _output["has_format"][0]
        position = _output["position"][0]
        line += " -o{} {}.{}".format(position, label, extension)
    return line


def build_parameter(parameters):
    line = ""
    for _parameter in parameters:
        _parameter = convert_object_to_dict(_parameter)
        if not _parameter.keys() >= KEYS_REQUIRED_PARAMETER:
            raise ValueError(f'{_parameter["id"]} has not the required information ')
        if "has_fixed_resource" in _parameter:
            value = _parameter["has_fixed_resource"][0]
        else:
            value = _parameter["has_default_value"][0]
        position = _parameter["position"][0]
        if 'has_data_type' not in  _parameter or _parameter["has_data_type"] is None or "string" in _parameter["has_data_type"]:
            line += " -p{} \"{}\"".format(position, value)
        else:
            line += " -p{} {}".format(position, value)

    return line

def create_sample_resource(_input, uri):
    _id = f"""https://w3id.org/okn/i/mint/${str(uuid.uuid4())}"""
    s = SampleResource(id=_id,
                       data_catalog_identifier="FFF-3s5c112e-c7ae-4cda-ba23-2e4f2286a18o",
                       value=[uri])
    _input.has_fixed_resource = [s.to_dict()]
