import logging

from mic._model_catalog_utils import get_label_from_response, create_request, get_existing_resources
from mic.drawer import print_request, print_choices, show_values_complex, show_values
from mic.file import save
from mic._utils import first_line_new
from mic._mappings import *

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
    select_property = click.prompt(
        "Select the property to edit [{}-{}] or [show, save, send, load, exit]".format(1, len(properties_choices)),
        default=1,
        show_choices=False,
        type=click.Choice(list(range(1, len(properties_choices) + 1)) + actions_choices),
        value_proc=parse
        )
    # TO DO: make sure selected action is within valid range!
    return select_property


def push_menu(request):
    pass


def handle_actions(request, action):
    if type(action) != str:
        return False
    if action == ACTION_CHOICES[0]:
        save(request)
    elif action == ACTION_CHOICES[1]:
        push_menu(request)
    elif action == ACTION_CHOICES[2]:
        pass
    return True


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
    default_value = default_value[0] if isinstance(default_value, list) else default_value

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
    resources.pop(choice - 1)


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
