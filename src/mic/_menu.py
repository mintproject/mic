import logging

import click
from mic._person import PersonCli
from mic._utils import first_line_new
from mic._mappings import *
from modelcatalog import ApiException
from tabulate import tabulate
import json

COMPLEX_CHOICES = ["select", "add", "edit", "remove"]
ACTION_CHOICES = ["save", "send", "exit"]


def edit_menu(property_chosen, request, resource_name, mapping):
    try:
        var_selected = list(mapping.keys())[property_chosen - 1]
        ask_value(request, var_selected, resource_name=resource_name, mapping=mapping)
    except Exception as e:
        logging.error(e, exc_info=True)
    except click.Abort:
        click.echo("The option chosen is not supported")
        input("press any key to continue")



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


def select_enable(mapping):
    if SELECT in mapping and mapping[SELECT]:
        return mapping[SELECT]
    return False


def get_existing_resources(resource_name):
    # TO DO: clean up this, it's not too maintainable
    if (resource_name == "Author") or (resource_name == "Contributor") or (resource_name == "Contact person"):
        try:
            return PersonCli().get()
        except ApiException as e:
            click.echo("Failed to get person resources")



def select_existing_resources(var_selected, resource_name, mapping):
    click.echo("Available resources")
    response = get_existing_resources(var_selected)
    resources = get_label_from_response(response)
    print_choices(resources)
    if click.confirm("Did you find the {}?".format(var_selected), default=True):
        choice = click.prompt("Select the {}".format(var_selected),
                              default=1,
                              show_choices=False,
                              type=click.Choice(list(range(1, len(resources) + 1))),
                              value_proc=parse
                              )
        return response[choice - 1].to_dict()
    return None


def show_menu(request):
    selection = click.prompt("Which property would you like to show?",
                             default=1,
                             show_choices=False,
                             type=click.Choice(list(range(1, len(request.keys()) + 1))),
                             value_proc=parse
                             )
    # TO DO: make sure selected variable is within range
    var_selected = list(request.keys())[selection - 1]
    print('Current value for ' + var_selected + ' is: ' + str(request[var_selected]))
    input('Press any key to continue')


def select_property_menu(request, resource_name, mapping):
    """
    Select the property to edit
    """
    print_request(request, mapping)
    properties_choices = list(request.keys())
    actions_choices = ["show", "save", "send", "load", "exit"]
    choices = properties_choices + actions_choices
    select_property = click.prompt("Select the property to edit [{}-{}] or [show, save, send, load, exit]".format(1, len(properties_choices)),
                          default=1,
                          show_choices=False,
                          type=click.Choice(list(range(1, len(properties_choices) + 1)) + actions_choices),
                          value_proc=parse
                          )
    # TO DO: make sure selected action is within valid range!
    return select_property


def handle_actions(request, action):
    if type(action) != str:
        return False
    if action == ACTION_CHOICES[0]:
        save_menu(request)
    elif action == ACTION_CHOICES[1]:
        push_menu(request)
    elif action == ACTION_CHOICES[2]:
        pass
    return True


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


def print_request(request, mapping):
    table = []
    headers = ["no.", "Property", "Value"]
    i = 1
    for key, value in mapping.items():
        prop_mapping = get_prop_mapping(mapping, key)
        if prop_mapping in request:
            request_value = request[prop_mapping]
        else:
            request_value = None
        # A complex property has multiple dict inside.
        if request_value and isinstance(request_value, list) and isinstance(request_value[0], dict):
            short_value = ' '.join(
                [str(elem["label"]) if "label" in elem else "Item without label" for elem in request_value])
        else:
            short_value = (
                request_value if (request_value is None or len(str(request_value)) < 50) else str(request_value)[
                                                                                              :50] + "...")
        table.append([i, key, short_value])
        i = i + 1
    print(tabulate(table, headers, tablefmt="grid"))


def print_choices(choices):
    for index, choice in enumerate(choices):
        click.echo("[{}] {}".format(index + 1, choice))


def remove_menu(request):
    pass


def save_menu(request):
    """
    Function to save the current request as a JSON file
    :param request: JSON to save
    :return:
    """
    try:
        # print_request(request)
        file_name = click.prompt('Enter the file name to save: ')
        file_name += '.json'
        with open(file_name, 'w') as outfile:
            json.dump(request, outfile)
        print('File saved successfully')
        # this will show status if saved.
        # click.confirm('File saved successfully. Do you want to continue editing?', abort=True)
    except:
        print('An error occurred when saving the file')
    pass


def load_menu(request):
    """
    Method that loads a JSON file of a model
    TO DO: Does not distinguish type at the moment (assumes it's a model)
    :param request: Current JSON request (initialized)
    :return: the JSON with the loaded file in request
    """
    try:
        file = click.prompt("Please type the path if the file to load")
        with open(file) as json_file:
            loaded_file = json.load(json_file)
        print('File loaded successfully')
    except:
        print('Error when loading the file')
        # click.confirm('Error loading the file. Continue?', abort=True)
    # print_request(request)
    # click.prompt('Press enter to continue',default='a')
    return loaded_file


def push_menu(request):
    pass


def parse(value):
    try:
        return int(value)
    except:
        return value


def ask_value(request, variable_name, resource_name, mapping, default_value="", select=None):
    """
    Modifies the request
    """
    request_property = get_prop_mapping(mapping, variable_name)
    click.clear()

    if is_complex(mapping, variable_name):
        show_values_complex(mapping, request, request_property, variable_name)
        actions_complex(mapping, request, request_property, resource_name, select, variable_name)
    else:
        show_values(mapping, request, request_property, variable_name)
        set_value(mapping, request, request_property, resource_name, variable_name)


def actions_complex(mapping, request, request_property, resource_name, select, variable_name):
    choices_new = COMPLEX_CHOICES.copy()
    if request[request_property] is None:
        choices_new.remove("edit")
        choices_new.remove("remove")

    choice = click.prompt("Select action:",
                          default=choices_new[0],
                          show_choices=True,
                          type=click.Choice(choices_new),
                          value_proc=parse
                          )
    if choice == COMPLEX_CHOICES[0]:
        select_value_complex(mapping, request, request_property, resource_name, variable_name)
    elif choice == COMPLEX_CHOICES[1]:
        create_value_complex(mapping, request, request_property, resource_name, variable_name)
    elif choice == COMPLEX_CHOICES[2]:
        edit_value_complex(request[request_property], mapping, resource_name, variable_name)
    elif choice == COMPLEX_CHOICES[3]:
        delete_value_complex(request[request_property])
    return choice


def set_value(mapping, request, request_property, resource_name, variable_name):
    default_value = request[request_property] if request_property in request and request[request_property] else None
    default_value = default_value[0] if isinstance(default_value,list) else default_value

    value = ask_simple_value(variable_name, resource_name, mapping[variable_name], default_value=default_value)
    if value:
        request[request_property] = [value]


def select_value_complex(mapping, request, request_property, resource_name, variable_name):
    value = None
    if select_enable(mapping[variable_name]):
        sub_resource = select_existing_resources(variable_name, resource_name, mapping)
        value = sub_resource if sub_resource else ask_complex_value(variable_name, resource_name, mapping)
    elif not request[request_property]:
        value = ask_complex_value(variable_name, resource_name, mapping)
    if request[request_property] is None:
        request[request_property] = [value]
    else:
        request[request_property].append(value)


def create_value_complex(mapping, request, request_property, resource_name, variable_name):
    value = ask_complex_value(variable_name, resource_name, mapping)
    if request[request_property] is None:
        request[request_property] = [value]
    else:
        request[request_property].append(value)

def edit_value_complex(request, mapping, resource_name, variable_name):
    labels = get_label_from_response(request)
    print_choices(labels)
    
    choice = click.prompt("Select the resource to edit",
                          default=1,
                          show_choices=False,
                          type=click.Choice(list(range(1, len(labels) + 1))),
                          value_proc=parse
                          )
    request_var = get_prop_mapping(mapping, variable_name)
    edit_resource(request, mapping, variable_name, request_var)

def delete_value_complex(resources):
    labels = get_label_from_response(resources)
    print_choices(labels)
    choice = click.prompt("Select the resource to delete",
                          default=1,
                          show_choices=False,
                          type=click.Choice(list(range(1, len(labels) + 1))),
                          value_proc=parse
                          )
    resources.pop(choice-1)

def set_value_complex(mapping, request, request_property, resource_name, select, variable_name):
    value = None
    if select is None and select_enable(mapping[variable_name]):
        sub_resource = select_existing_resources(variable_name, resource_name, mapping)
        value = sub_resource if sub_resource else ask_complex_value(variable_name, resource_name, mapping)
    elif not request[request_property]:
        value = ask_complex_value(variable_name, resource_name, mapping)
    if request[request_property] is None:
        request[request_property] = [value]
    else:
        request[request_property].append(value)


def show_values(mapping, request, request_property, variable_name):
    if request_property in request and request[request_property]:
        click.echo('Current value for ' + variable_name + ' is: ' + str(request[request_property]))
    else:
        click.echo('No value for {}'.format(variable_name))


def show_values_complex(mapping, request, request_property, variable_name):
    if request[request_property]:
        for resource in request[request_property]:
            click.echo(resource["label"])
    else:
        click.echo('No value for {}'.format(variable_name))


def get_prop_mapping(mapping, variable_selected):
    return mapping[variable_selected]["id"]


def ask_complex_value(variable_name, resource_name, mapping, default_value=""):
    prop = mapping[variable_name]["id"]
    if prop == "has_version":
        resource = add_resource(mapping_model_version, SoftwareVersion)
    elif (prop == "author") or (prop == "contributor") or (prop == "has_contact_person"):
        resource = add_resource(mapping_person, Person)
    elif prop == "logo":
        resource = add_resource(mapping_image, Image)
    return resource


def ask_simple_value(variable_name, resource_name, mapping, default_value=""):
    get_definition(mapping, variable_name)
    value = click.prompt('{} - {} '.format(resource_name, variable_name), default=default_value)
    if value:
        return value
    else:
        return None


def add_resource(mapping, resource_name):
    request = create_request(mapping.values())
    while True:
        click.clear()
        first_line_new(resource_name)
        property_chosen = select_property_menu(request, resource_name, mapping)
        if handle_actions(request, property_chosen):
            break
        property_mcat_selected = list(mapping.keys())[property_chosen - 1]
        ask_value(request, property_mcat_selected, resource_name=resource_name, mapping=mapping)


def edit_resource(request, mapping, resource_name, request_var):
    while True:
        if (request_var == "author") or (request_var == "contributor"):
            mapping = mapping_person
            resource_name = "Person"
        property_chosen = select_property_menu(request[0], resource_name, mapping)
        if handle_actions(request, property_chosen):
            break
        property_mcat_selected = list(mapping.keys())[property_chosen - 1]
        ask_value(request[0], property_mcat_selected, resource_name=resource_name, mapping=mapping)


