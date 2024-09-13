import click

from .cli.ask import ask
from .cli.setup import setup


@click.group()
def cli():
    pass

cli.add_command(ask)
cli.add_command(setup)

if __name__ == "__main__":
    cli()
