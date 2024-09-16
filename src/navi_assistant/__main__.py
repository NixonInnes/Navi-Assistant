# src/navi_assistant/__main__.py

import click

from .cli.ask import ask
from .cli.config import config
from .cli.files import files
from .cli.info import info
from .cli.init import init
from .cli.sync import sync
from .cli.tools import tools


@click.group()
def cli():
    """·.•°•.·.✧ ✦ 🧚 ✦ [ Navi Assistant CLI ]

    Navi is an OpenAI assistant manager which allows you to quickly create assistants with useful tools and query them.

    Navi provides a global assistant and local assistants. The global assitant is system-wide, and local assistants are specific
    to a directory. You can create a local assistant by running `navi init` in a directory.
    When you use Navi, it will check for a local assistant first, and if it doesn't exist, it will use the global 
    assistant.
    """
    pass

cli.add_command(ask)
cli.add_command(config)
cli.add_command(files)
cli.add_command(info)
cli.add_command(init)
cli.add_command(sync)
cli.add_command(tools)

if __name__ == "__main__":
    cli()
