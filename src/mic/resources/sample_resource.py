import modelcatalog
from mic.model_catalog_utils import get_api
from modelcatalog import ApiException


RESOURCE = "Input"


class SampleResourceCli:
    name = RESOURCE

    def __init__(self, profile=None):
        self.profile = profile

    def get(self):
        api, username = get_api(profile=self.profile)
        api_instance = modelcatalog.SampleResourceApi(api)
        try:
            # List all Person entities
            api_response = api_instance.sampleresources_get(username=username)
            return api_response
        except ApiException as e:
            raise e

