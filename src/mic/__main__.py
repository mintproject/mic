"""Main file for cmd
"""

import collections
import sys
from pathlib import Path
import click
import mic
import semver
from mic import _utils
from mic.click_encapsulate.commands import start, trace, configs,\
    add_parameters, inputs, outputs, run, upload, wrapper
from mic.commands_notebook import read, upload_image, upload_component
from mic.credentials import configure_credentials, print_list_credentials
from modelcatalog import Configuration


@click.group()
@click.option("--verbose", "-v", default=0, count=True)
def cli(verbose):
    _utils.init_logger()
    if verbose:
        pass
    try:
        lv = ".".join(_utils.get_latest_version().split(".")[:3])
    except Exception as e:
        click.secho(
            f"""WARNING: Unable to check if MIC is updated""",
            fg="yellow",
        )
        return

    cv = ".".join(mic.__version__.split(".")[:3])

    if semver.compare(lv, cv) > 0:
        click.secho(
            f"""WARNING: You are using mic version {mic.__version__}, however version {lv} is available.
You should consider upgrading via the 'pip install --upgrade mic' command.""",
            fg="yellow",
        )


@cli.command(short_help="Show mic version")
def version(debug=False):
    click.echo(f"{Path(sys.argv[0]).name} v{mic.__version__}")


@cli.command(short_help="Configure credentials", help="Configure your credentials to access the Model Catalog API, "
                                                      "and Docker features")
@click.option(
    "--profile",
    "-p",
    envvar="MINT_PROFILE",
    type=str,
    default="default",
    metavar="<profile-name>",
)
@click.option('--server', prompt='Model Catalog API',
              help='The Model Catalog API', required=True, default=Configuration().host, show_default=True)
@click.option('--username', prompt='Username',
              help='Your email', required=True, default="mint@isi.edu", show_default=True)
@click.option('--password', prompt="Password",
              required=True, hide_input=True, help="Your password")
@click.option('--name', prompt='Name', help='Your name', required=True)
@click.option('--dockerhub_username', prompt='Docker Username', help='Your Docker Username')
def credentials(server, username, password, name, dockerhub_username, profile="default"):
    try:
        email = username
        configure_credentials(server, username, password, name, email, dockerhub_username, profile)
    except Exception as e:
        click.secho("Unable to create configuration file", fg="red")


@cli.command(short_help="List credentials profiles",
             help="List credential parameters for mic profiles. Lists all profile credentials if no profile given")
@click.option(
    "--profile",
    "-p",
    envvar="MINT_PROFILE",
    type=str,
    default=None,
    metavar="<profile-name>",
    help="specify a profile to list"
)
@click.option(
    "--short",
    "-s",
    is_flag=True,
    help="Only show a list of profiles, not their contents"
)
def list_credentials(profile=None, short=False):
    print_list_credentials(profile, short)


class OrderedGroup(click.Group):
    def __init__(self, name=None, commands=None, **attrs):
        super(OrderedGroup, self).__init__(name, commands, **attrs)
        #: the registered subcommands by their exported names.
        self.commands = commands or collections.OrderedDict()

    def list_commands(self, ctx):
        return self.commands

@cli.group(cls=OrderedGroup)
def pkg():
    """Command to encapsulate your model component"""


@cli.group(cls=OrderedGroup)
def notebook():
    """Command to encapsulate your jupyter notebook. BETA VERSION"""

pkg.add_command(start)
pkg.add_command(trace)
pkg.add_command(add_parameters)
pkg.add_command(configs)
pkg.add_command(inputs)
pkg.add_command(outputs)
pkg.add_command(wrapper)
pkg.add_command(run)
pkg.add_command(upload)



notebook.add_command(read)
notebook.add_command(upload_image)
notebook.add_command(upload_component)
