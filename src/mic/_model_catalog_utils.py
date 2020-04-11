import click
from modelcatalog import ApiException
from mic._person import PersonCli

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
        if isinstance(resource,dict):
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

def get_existing_resources(resource_name):
    """
    Get all the resources of a resource
    @param resource_name: The name of the resource (mic spec, not modelcatalog)
    @type resource_name:
    @return: A list of resource
    @rtype: List[]
    """
    # TO DO: clean up this, it's not too maintainable
    if (resource_name == "Author") or (resource_name == "Contributor") or (resource_name == "Contact person"):
        try:
            return PersonCli().get()
        except ApiException as e:
            click.echo("Failed to get person resources")
