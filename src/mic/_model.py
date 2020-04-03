import logging
import modelcatalog
from mic._utils import ask_simple_value, get_api_configuration, first_line_new
from mic._person import add_person


from mic._model_version import create as create_model_version
from modelcatalog import ApiException
import click

mapping_parameter = {
    'Short Description': 'label',
    'Value': 'hasFixedValue',
}

mapping_model = {
    'Name': 'label',
    'Short Description': 'label',
    'keywords': 'keywords',
    'website': 'website',
    'documentation': 'documentation',
}

RESOURCE = "Model"
def create():
    model_versions = []
    click.echo("Adding a new Model")
    first_line_new(RESOURCE)
    request = {}
    for key in mapping_model:
        value = ask_simple_value(key, RESOURCE)
        request[mapping_model[key]] = value

    request["author"] = add_person("Author")
    request["contributor"] = add_person("contributors")

    first_line_new(RESOURCE)
    while click.confirm('Do you want create a new version for the model?'):
        model_versions.append(create_model_version())
        if not click.confirm('Do you want create another version for the model?'):
            break
    request["hasVersion"] = model_versions
    push(request)




def push(request):
    configuration, username = get_api_configuration()
    api_instance = modelcatalog.ModelApi(modelcatalog.ApiClient(configuration=configuration))
    try:
        api_response = api_instance.models_post(username, model=request)
    except ApiException as e:
        logging.error("Exception when calling ModelConfigurationSetupApi->modelconfigurationsetups_post: %s\n" % e)
        quit()
    print(api_response)


