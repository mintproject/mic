import modelcatalog
from mic._utils import get_api, first_line_new
import click
from modelcatalog import ApiException

RESOURCE = "Person"
RESOURCE_AUTHOR = "Author"


class PersonCli:
    def __init__(self):
        pass

    @staticmethod
    def get():
        # create an instance of the API class
        api, username = get_api()
        api_instance = modelcatalog.PersonApi(api)
        try:
            # List all Person entities
            api_response = api_instance.persons_get(username=username)
            return api_response
        except ApiException as e:
            raise e
