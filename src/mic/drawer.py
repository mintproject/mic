import click
from mic._mappings import get_prop_mapping
from tabulate import tabulate


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


def show_values_complex(request, request_property, variable_name):
    if request[request_property]:
        for resource in request[request_property]:
            click.echo(resource["label"])
    else:
        click.echo('No value for {}'.format(variable_name))


def show_values(request, request_property, variable_name):
    if request_property in request and request[request_property]:
        click.echo('Current value for ' + variable_name + ' is: ' + str(request[request_property]))
    else:
        click.echo('No value for {}'.format(variable_name))

def show_error(request_message):
    click.secho(request_message, fg="red")