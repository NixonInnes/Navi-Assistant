# src/navi_assistant/cli/config.py

from typing import get_type_hints

import click

from .. import ai
from ..config import NaviConfig
from ..navi import Navi
from ..style import art, messaging


@click.command()
@click.option(
    "--global", "use_global", is_flag=True, help="Use the global configuration"
)
@click.argument("key", type=str)
@click.argument("value", type=str)
def config(use_global: bool, key: str, value: str):
    """Modify the assistant configuration."""
    click.echo(art.styled_fairy + messaging.make_header("Config"))
    navi = Navi(use_global)

    if navi.is_global:
        click.echo(messaging.make_warning("Global configuration"))
    else:
        click.echo(messaging.make_info("Local configuration"))

    if key not in [k for k, v in get_type_hints(NaviConfig).items() if v is str]:  # pyright: ignore[reportAny]
        click.echo(messaging.make_error(f"Invalid configuration key: {key}"))
        return

    navi.config[key] = value
    click.echo(messaging.make_info(f"Set {key} to {value}"))
    navi.save_config()

    client = ai.get_client()

    ai.update_assistant(
        client,
        navi.config["assistant_id"],
        navi.config["name"],
        navi.config["model"],
        navi.config["instructions"],
        navi.tools_dir,
    )
