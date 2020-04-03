import modelcatalog
from mic._utils import ask_simple_value, get_api_configuration, first_line_new
import click

attribute_map = {
    'name': 'label',
    'email': 'email',
    'website': 'website'
}

RESOURCE = "Person"
RESOURCE_AUTHOR = "Author"

def add_person(resource):
    first_line_new(resource)
    persons = []
    question_add = click.confirm('Do you want add a {} to the model?'.format(resource))
    while question_add:
        persons.append(menu())
        if not click.confirm('Do you want add another {} to the model?'.format(resource)):
            break
    return persons


def create():
    request = {}
    for key in attribute_map:
        value = ask_simple_value(key, RESOURCE_AUTHOR)
        request[attribute_map[key]] = value
    return request


def parse(value):
    return value

def select(resource):
    first_line_new(resource)
    options = _list()
    authors = []
    authors2 = []
    i = 0
    for d in options:
        if "label" in d.to_dict():
            authors.append(d.label[0])
            authors2.append(d.to_dict())
            i += 1
            click.echo("[{}] {}".format(i, authors[i-1]))

    action = click.prompt("Please select the author",
                          default=1,
                          show_choices=False,
                          type=click.Choice(range(1,i)),
                          value_proc=parse
                          )
    click.echo("Selected {}".format(authors2[int(action)-1]["label"][0]))
    return authors2[int(action)-1]

def _list():
    configuration, username = get_api_configuration()
    api_instance = modelcatalog.PersonApi(modelcatalog.ApiClient(configuration=configuration))
    api_response = api_instance.persons_get(username=username)
    return api_response

def menu():
    options = ["create", "select"]
    action = click.prompt("Please select a option about the Author", default=options[0], type=click.Choice(options))
    if action == "select":
        return select(RESOURCE_AUTHOR)
    else:
        return create()