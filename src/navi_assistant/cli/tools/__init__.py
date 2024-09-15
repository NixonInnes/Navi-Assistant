import click

from .pull import pull


@click.group()
def tools():
    """Modify the assistant tools."""
    pass

tools.add_command(pull)
