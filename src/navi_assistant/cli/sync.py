import click

from .. import ai
from ..config import config_handler

@click.command()
@click.option("--global", "use_global", is_flag=True, help="Use the global configuration")
def sync(use_global: bool):
    """Sync the assistant configuration with OpenAI."""
    _, config = config_handler.load(force_global=use_global)

    client = ai.get_client()

    # TODO: Include commands in the sync
    _ = client.beta.assistants.update(
        assistant_id=config["assistant_id"],
        name=config["name"],
        model=config["model"],
        instructions=config["instructions"],
    )


