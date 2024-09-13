import click
from typing import get_type_hints

from ..style import art, messaging
from ..config import NaviConfig, config_handler

@click.command()
@click.option("--global", "use_global", is_flag=True, help="Use the global configuration")
@click.argument("key", type=str)
@click.argument("value", type=str)
def config(use_global: bool, key: str, value: str):
    """Modify the assistant configuration."""
    click.echo(art.styled_fairy + messaging.make_header("Config"))
    is_global, config = config_handler.load(force_global=use_global)

    if is_global:
        click.echo(messaging.make_warning("Global configuration"))
    else:
        click.echo(messaging.make_info("Local configuration"))

    if key not in [k for k,v in get_type_hints(NaviConfig).items() if v is str]:
        click.echo(messaging.make_error(f"Invalid configuration key: {key}"))
        return
    
    config[key] = value
    click.echo(messaging.make_info(f"Set {key} to {value}"))
    config_handler.save(config, force_global=use_global)

    # TODO: automatically sync with OpenAI

