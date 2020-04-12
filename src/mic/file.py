import json
import logging
import click


def clean_null_terms(d):
    """
    Recursively remove all None values from dictionaries and lists, and returns
    the result as a new dictionary or list.
    """
    if isinstance(d, list):
        return [clean_null_terms(x) for x in d if x is not None]
    elif isinstance(d, dict):
        return {
            key: clean_null_terms(val)
            for key, val in d.items()
            if val is not None
        }
    else:
        return d


def save(request):
    """
    Function to save the current request as a JSON file
    :param request: JSON to save
    :return:
    """
    try:
        file_name = click.prompt('Enter the file name to save (without extension): ')
        file_name += '.json'
        # Remove nulls
        request_dump = clean_null_terms(request)
        with open(file_name, 'w') as outfile:
            json.dump(request_dump, outfile)
        print('File saved successfully')
        # this will show status if saved.
        # click.confirm('File saved successfully. Do you want to continue editing?', abort=True)
    except Exception as err:
        logging.info(err, exc_info=True)
        click.secho(f"An error occurred when saving the file", fg="red")
    click.secho(f"Success", fg="green")
    return file_name


def load():
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
        click.echo('File loaded successfully')
    except:
        click.echo('Error when loading the file')
        return None
        # click.confirm('Error loading the file. Continue?', abort=True)
    return loaded_file
