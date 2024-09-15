import click

from .. import ai
from ..navi import Navi
from ..style import art, messaging

@click.command()
@click.option("--global", "use_global", is_flag=True, help="Use the global configuration")
def sync(use_global: bool):
    """Sync the assistant configuration with OpenAI."""
    click.echo(art.styled_fairy + messaging.make_header("Sync"))
    
    navi = Navi(use_global)

    client = ai.get_client()

    ai.update_assistant(
        client,
        assistant_id=navi.config["assistant_id"],
        name=navi.config["name"],
        model=navi.config["model"],
        instructions=navi.config["instructions"],
        tools_dir=navi.tools_dir,
    )


