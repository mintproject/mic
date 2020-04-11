import json
import logging
import click


def cleanNullTerms(d):
    clean = {}
    if d is not None:
        for k, v in d.items():
            if isinstance(v, dict):
                nested = cleanNullTerms(v)
                if len(nested.keys()) > 0:
                    clean[k] = nested
            elif v is not None:
                clean[k] = v
    return clean


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
        request_dump = cleanNullTerms(request)
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
