import os

import click

from ..navi import Navi
from ..style import art, messaging


@click.command()
@click.option(
    "--global", "use_global", is_flag=True, help="Use the global configuration"
)
def info(use_global: bool):
    """Display information about the assistant."""
    click.echo(art.styled_fairy + messaging.make_header("Info"))

    navi = Navi(use_global)

    if navi.is_global:
        click.echo(messaging.make_warning("Global configuration"))
    click.echo(messaging.make_info(f"Name: {navi.config['name']}"))
    click.echo(messaging.make_info(f"Description: {navi.config['description']}"))
    click.echo(messaging.make_info(f"Model: {navi.config['model']}"))
    click.echo(messaging.make_info(f"Assistant ID: {navi.config['assistant_id']}"))
    click.echo(messaging.make_info(f"Thread ID: {navi.config['thread_id']}"))
    click.echo(messaging.make_info("Available Commands:"))
    for tool in os.listdir(navi.tools_dir):
        tool = os.path.splitext(tool)[0]
        click.echo(messaging.make_info(f"  - {tool}"))
