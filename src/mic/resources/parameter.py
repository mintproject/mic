RESOURCE = "Parameter"


class ParameterCli:
    name = RESOURCE

    def __init__(self):
        pass

    # @staticmethod
    # def get():
    #     # create an instance of the API class
    #     api, username = get_api()
    #     api_instance = modelcatalog.PersonApi(api)
    #     try:
    #         # List all Person entities
    #         api_response = api_instance.persons_get(username=username)
    #         return api_response
    #     except ApiException as e:
    #         raise e
    #
    # @staticmethod
    # def push(request):
    #     configuration, username = get_api()
    #     api_instance = modelcatalog.ParameterApi(modelcatalog.ApiClient(configuration=configuration))
    #     try:
    #         api_response = api_instance.models_post(username, model=request)
    #     except ApiException as e:
    #         logging.error("Exception when calling ParameterConfigurationSetupApi->modelconfigurationsetups_post: %s\n" % e)
    #         raise e
    #     return api_response
