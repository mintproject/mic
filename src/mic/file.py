import json
import click


def save(request):
    """
    Function to save the current request as a JSON file
    :param request: JSON to save
    :return:
    """
    try:
        # print_request(request)
        file_name = click.prompt('Enter the file name to save (without extension): ')
        file_name += '.json'
        # Remove nulls
        for key, value in list(request.items()):
            if value is None:
                request[key] = []
        with open(file_name, 'w') as outfile:
            json.dump(request, outfile)
        print('File saved successfully')
        # this will show status if saved.
        # click.confirm('File saved successfully. Do you want to continue editing?', abort=True)
    except:
        print('An error occurred when saving the file')
    pass


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
        print('File loaded successfully')
    except:
        print('Error when loading the file')
        # click.confirm('Error loading the file. Continue?', abort=True)
    return loaded_file
