# src/navi_assistant/cli/tools/pull.py

import subprocess

import click

from ... import ai
from ...navi import Navi
from ...style import art, messaging


@click.command()
@click.option(
    "--global", "use_global", is_flag=True, help="Use the global configuration"
)
@click.argument("repo", type=str)
def pull(repo: str, use_global: bool = False):
    """Pull a set of assistant tools from a GitHub repository."""
    click.echo(art.styled_fairy + messaging.make_header("Tools:Pull"))

    navi = Navi(use_global)

    click.echo(messaging.make_info(f"Pulling tools from {repo}..."))

    url = f"https://github.com/{repo}.git"

    if navi.is_global:
        click.echo(messaging.make_warning("Global configuration"))

    try:
        _ = subprocess.run(["git", "clone", url, navi.tools_dir])
    except subprocess.CalledProcessError:
        click.echo(messaging.make_error("Failed to pull tools."))
        return

    client = ai.get_client()
    ai.update_assistant(
        client,
        navi.config["assistant_id"],
        navi.config["name"],
        navi.config["model"],
        navi.config["instructions"],
        navi.tools_dir,
    )
