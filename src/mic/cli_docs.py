import click


def info_start_inputs():
    click.secho("Detecting the inputs of your model using the information obtained by the `trace` command.", fg="blue")
    click.secho("If the input is a directory, MIC is going to compress in a zipfile", fg="blue")



def info_step8():
    click.echo("This step publishes your code, DockerImage and ModelConfiguration")
