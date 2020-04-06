import click
from mic._person import PersonCli
from mic._utils import first_line_new
from mic._mappings import *
from modelcatalog import ApiException
from tabulate import tabulate
import json


def edit_menu(choice, request, resource_name, mapping):
    var_selected = list(request.keys())[choice - 1]
    click.echo('Current value for ' + var_selected + ' is: ' + str(request[var_selected]))
    ask_value(request, var_selected, resource_name=resource_name, mapping=mapping)

def get_label_from_response(response):
    labels = []
    for resource in response:
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
    if resource_name == "Author":
        try:
            return PersonCli().get()
        except ApiException as e:
            click.echo("Failing to get resources")

def select_existing_resources(var_selected, resource_name, mapping):
    click.clear()
    click.echo("Available resources")
    response = get_existing_resources(var_selected)
    resources = get_label_from_response(response)
    print_choices(resources)
    if click.confirm("Did you find the {}?".format(var_selected), default=True):
        choice = click.prompt("Select the {}".format(var_selected),
                              default=1,
                              show_choices=True,
                              type=click.Choice(list(range(1, len(resources) + 1))),
                              value_proc=parse
                              )
        return response[choice-1]
    return None

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


def ask_value(request, variable_name, resource_name, mapping, default_value=""):
    """
    Modifies the request
    """
    value = None
    request_property = get_prop_mapping(mapping, variable_name)
    if mapping[variable_name]["complex"] and select_enable(mapping[variable_name]):
        request[variable_name] = select_existing_resources(variable_name, resource_name, mapping)
    elif mapping[variable_name]["complex"] and not value:
        request[variable_name] = ask_complex_value(variable_name, resource_name, mapping)
    else:
        request[variable_name] = ask_simple_value(variable_name, resource_name, mapping[variable_name])


def get_prop_mapping(mapping, variable_selected):
    return mapping[variable_selected]["id"]

def ask_complex_value(variable_name, resource_name, mapping, default_value=""):
    sub_resource = create_request(mapping_model_version.keys())
    if mapping[variable_name]["id"] == "has_version":
        return add_resource(mapping_model_version, SoftwareVersion)
    elif mapping[variable_name]["id"] == "author" or "contributor" or "has_contact_person":
        return add_resource(mapping_person, Person)
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
