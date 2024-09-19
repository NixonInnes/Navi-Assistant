# src/navi_assistant/cli/files/set.py

import click

from ...navi import Navi
from ...style import art, messaging


@click.command()
@click.option(
    "--global", "use_global", is_flag=True, help="Use the global configuration"
)
@click.option(
    "--dir",
    "-d",
    type=str,
    required=False,
    multiple=True,
    help="List of directories to be searched for store files",
)
@click.option(
    "--file-ext",
    "-e",
    type=str,
    required=False,
    multiple=True,
    help="List of file extensions to be included in the store",
)
def set(dirs: list[str], file_exts: list[str], use_global: bool = False):
    """Set the store files for the assistant."""
    click.echo(art.styled_fairy + messaging.make_header("Tools:Files"))

    navi = Navi(use_global)

    if navi.is_global:
        click.echo(messaging.make_warning("Global configuration"))

    click.echo(
        messaging.make_info("Setting store file directories to: " + ", ".join(dirs))
    )
    click.echo(
        messaging.make_info("Setting store file extensions to: " + ", ".join(file_exts))
    )

    navi.config["store_folders"] = dirs
    navi.config["store_file_extensions"] = file_exts

    navi.save_config()

