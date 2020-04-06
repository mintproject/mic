import click
from mic._utils import first_line_new
from mic._mappings import *
from tabulate import tabulate
import json


def edit_menu(choice, request, resource_name, mapping):
    var_selected = list(request.keys())[choice - 1]
    print('Current value for ' + var_selected + ' is: ' + str(request[var_selected]))
    print('Insert new value (c to CANCEL)')
    response = ask_value(var_selected, resource_name=resource_name, mapping=mapping)
    if response != ["c"]:
        print(response)
        request[var_selected] = response


def show_menu(request):
    selection = click.prompt("Which property would you like to show?",
                             default=1,
                             show_choices=True,
                             type=click.Choice(list(range(1, len(request.keys()) + 1))),
                             value_proc=parse
                             )
    # TO DO: make sure selected variable is within range
    var_selected = list(request.keys())[selection - 1]
    print('Current value for ' + var_selected + ' is: ' + str(request[var_selected]))
    input('Press any key to continue')


def default_menu(request, resource_name, mapping):
    """
    First menu: Selection the action
    """
    print_request(request, mapping)
    properties_choices = list(request.keys())
    actions_choices = ["show", "save", "send", "load", "exit"]
    choices = properties_choices + actions_choices
    # print_choices(properties_choices)
    action = click.prompt("Select the property to edit",
                          default=1,
                          show_choices=True,
                          type=click.Choice(list(range(1, len(properties_choices) + 1)) + actions_choices),
                          value_proc=parse
                          )
    # TO DO: make sure selected action is within valid range!
    if type(action) == str:
        action = handle_actions(request, action)
    return action


def handle_actions(request, action):
    if action == "exit":
        return 0
    if action == "show":
        return -2
    if action == "save":
        save_menu(request)
    elif action == "send":
        push_menu(request)
    elif action == "load":
        req_aux = load_menu(request)
        # copy dictionary values (cannot assign to request directly)
        for key in request:
            request[key] = None
            if key in req_aux:
                request[key] = req_aux[key]
    return -1


def create_request(keys):
    """
    Create a dictionary to send the model catalog
    @param keys: List with properties of the resource
    @return: dict
    """
    request = {}
    for key in keys:
        request[key] = None
    return request


def print_request(request, mapping):
    table = []
    headers = ["no.", "Property", "Value", "Complex"]
    i = 1
    for key, value in request.items():
        # value is a list, not a string. We truncate at 50 char
        short_value = (value if (value is None or len(str(value)) < 50) else str(value)[:50] + "...")
        # print(len(str(value)))
        table.append([i, key, short_value, mapping[key]["complex"]])
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


def ask_value(variable_name, resource_name, mapping, default_value=""):
    if mapping[variable_name]["complex"]:
        value = ask_complex_value(variable_name, resource_name, mapping)
    else:
        value = ask_simple_value(variable_name, resource_name, mapping[variable_name])
    return value


def ask_complex_value(variable_name, resource_name, mapping, default_value=""):
    sub_resource = create_request(mapping_model_version.keys())
    if mapping[variable_name]["id"] == "has_version":
        return add_resource(mapping_model_version, SoftwareVersion)
    elif mapping[variable_name]["id"] == "author" or "contributor" or "has_contact_person":
        return add_resource(mapping_model_version, Person)
    pass


def ask_simple_value(variable_name, resource_name, entry, default_value=""):
    definition = entry['definition']
    required = entry['required']
    text_required = "[REQUIRED]"
    if variable_name.lower() == "name":
        default_value = None
    if not required:
        text_required = "[OPTIONAL]"
    #   value = click.prompt('{} - {} '.format(resource_name, variable_name), default=default_value)
    value = click.prompt('{} - {} [DEFINITION : {}]'.format(resource_name, variable_name,
                                                            definition) + ' ' + text_required + '\n',
                         default=default_value)
    if value:
        return [value]
    else:
        return []


def add_resource(mapping, resource_name):
    request = create_request(mapping.keys())
    while True:
        click.clear()
        # print(mapping)
        first_line_new(resource_name)
        choice = default_menu(request, resource_name, mapping)
        if choice == 0:
            # exit
            break
        elif choice == -1:
            # Save, send, load (do not finish)
            # click.confirm("Continue editing?", abort=True)
            continue
        elif choice == -2:
            # Show a definition of the current resource
            show_menu(request)
        else:
            edit_menu(choice, request, resource_name, mapping)
    return [request]
