import click


def print_choices(choices):
    for index, choice in enumerate(choices):
        click.echo("[{}] {}".format(index + 1, choice))

