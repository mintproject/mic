import configparser
import os
import pathlib
from mic.constants import DEFAULT_CONFIGURATION_WARNING
__DEFAULT_MINT_API_CREDENTIALS_FILE__ = "~/.mint/credentials"

import click

DEFAULT_PROFILE = "default"


def get_credentials(profile: str) -> dict:
    credentials_file = pathlib.Path(
        os.getenv("MINT_CREDENTIALS_FILE", __DEFAULT_MINT_API_CREDENTIALS_FILE__)
    ).expanduser()
    credentials = configparser.ConfigParser()
    if credentials_file.exists():
        credentials.read(credentials_file)
        return credentials[profile]
    elif credentials is not None and profile not in credentials and profile != ("%s" % DEFAULT_PROFILE):
        click.secho(DEFAULT_CONFIGURATION_WARNING + " {}".format(profile), fg="yellow")
    raise ValueError("Profile doesn't exists")


def configure_credentials(server, username, password, git_username, git_token, name, email, dockerhub_username, profile):
    credentials_file = pathlib.Path(
        os.getenv("MINT_CREDENTIALS_FILE", __DEFAULT_MINT_API_CREDENTIALS_FILE__)
    ).expanduser()
    os.makedirs(str(credentials_file.parent), exist_ok=True)

    credentials = configparser.ConfigParser()
    credentials.optionxform = str

    if credentials_file.exists():
        credentials.read(credentials_file)

    credentials[profile] = {
        "server": server,
        "username": username,
        "password": password,
        "git_username": git_username,
        "git_token": git_token,
        "name": name,
        "email": email,
        "dockerhub_username": dockerhub_username,
    }

    with credentials_file.open("w") as fh:
        credentials_file.parent.chmod(0o700)
        credentials_file.chmod(0o600)
        credentials.write(fh)


def print_list_credentials(profile, short):

    credentials_file = pathlib.Path(
        os.getenv("MINT_CREDENTIALS_FILE", __DEFAULT_MINT_API_CREDENTIALS_FILE__)
    ).expanduser()
    credentials = configparser.ConfigParser()
    if credentials_file.exists():
        credentials.read(credentials_file)
    else:
        click.secho(DEFAULT_CONFIGURATION_WARNING + " {}".format(profile),
                    fg="yellow")

    profile_list = []

    # list all profiles if none given
    if profile is None:
        for p in credentials:
            # configparser has both DEFAULT and default read, no need to get both
            if p != "DEFAULT":
                profile_list.append(get_credentials(p))
    # list given profile
    else:
        try:
            profile_list.append(get_credentials(profile))
        except KeyError as e:
            click.secho(DEFAULT_CONFIGURATION_WARNING + " {}".format(profile), fg="yellow")

    click.echo("\n== Profiles ==")
    if not short:
        click.echo("")
    for prof in profile_list:
        # list profile name
        # there is no way to get the key from the prof obj, so I have to manually format the tostring
        click.secho("[{}]".format(prof.__str__().split(" ")[1].split(">")[0]), fg="blue")

        # Only show details if short is not used
        if not short:
            for field in prof:
                # Dont print password or token
                if field != "password" and field != "git_token":
                    click.secho("   {}".format(field), nl=False, fg="green")
                    click.secho(": {}".format(prof[field]))
                # Dont print full token for security reasons
                elif field == "git_token":
                    # Its safe to print if its obviously not a github token
                    if len(prof[field]) < 6:
                        click.secho("   {}".format(field), nl=False, fg="green")
                        click.secho(": {}".format(prof[field]))

                    else:
                        click.secho("   {}".format(field), nl=False, fg="green")
                        click.secho(": Ending in \"...{}\"".format((prof[field])[-5:]))
            click.echo("\n")
