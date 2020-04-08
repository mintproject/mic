import click
from modelcatalog import ApiException
from mic.resources._person import PersonCli


def get_label_from_response(response):
    labels = []
    for resource in response:
        if isinstance(resource, dict):
            resource_dict = resource
        else:
            resource_dict = resource.to_dict()
        if "label" in resource_dict:
            labels.append(resource_dict["label"][0])
        elif "id" in resource_dict:
            labels.append(resource_dict["id"])
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
    # TO DO: clean up this, it's not too maintainable
    if (resource_name == "Author") or (resource_name == "Contributor") or (resource_name == "Contact person"):
        try:
            return PersonCli().get()
        except ApiException as e:
            click.echo("Failed to get person resources")
