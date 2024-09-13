import click

from .cli.ask import ask
from .cli.config import config
from .cli.info import info
from .cli.init import init
from .cli.sync import sync


@click.group()
def cli():
    """Navi Assistant CLI
    Navi is an OpenAI assistant manager which allows you to quickly create assistants with useful tools and query them.

    By default, interacting with an assistant will use the global assistant.
    You can also create "local" assistants which are stored in the current directory. When you use a Navi command,
    it will check if there is a local assistant in the current directory and use that instead of the global assistant.
    """
    pass

cli.add_command(ask)
cli.add_command(config)
cli.add_command(info)
cli.add_command(init)
cli.add_command(sync)

if __name__ == "__main__":
    cli()
