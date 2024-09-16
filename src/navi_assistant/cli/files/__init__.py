# src/navi_assistant/cli/tools/__init__.py

import click

from .set import set
from .sync import sync


@click.group()
def files():
    """Modify the assistant files."""
    pass

files.add_command(set)
files.add_command(sync)
