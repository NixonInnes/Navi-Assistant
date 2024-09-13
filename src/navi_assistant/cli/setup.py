import click
from openai import OpenAI

from .. import ai
from ..cache import NaviCache, load_cache, save_cache
from ..config import NaviConfig, load_config, save_config
from ..style import art, messaging

@click.command()
def setup():
    click.echo(art.styled_fairy + messaging.make_header("Setup"))
    config = load_config()
    cache = load_cache()

    # Setup API Key
    setup_api_key(config)

    # Create OpenAI Client
    client = ai.get_client(config["api_key"])

    # Setup Assistant ID
    setup_assistant(config, cache, client)

    # Create thread
    thread_id = ai.create_thread(client)
    config["thread_id"] = thread_id

    # Save Config
    save_config(config)
    save_cache(cache)


def setup_api_key(config: NaviConfig) -> None:
    if existing_key := config["api_key"]:
        click.echo(
            messaging.make_warning(
                f"API Key already exists in config file: {existing_key}"
            )
        )
        if not click.confirm(
            messaging.make_prompt("Do you want to overwrite the existing API Key?")
        ):
            return

    api_key: str = click.prompt(messaging.make_prompt("Enter OpenAI API Key"), type=str)
    config["api_key"] = api_key


def setup_assistant(config: NaviConfig, cache: NaviCache, client: OpenAI) -> None:
    if existing_id := config["assistant_id"]:
        click.echo(
            messaging.make_warning(
                f"Assistant ID already exists in config file: {existing_id}"
            )
        )
        if not click.confirm(
            messaging.make_prompt("Do you want to overwrite the existing Assistant ID?")
        ):
            return

    if click.confirm(messaging.make_prompt("Do you want to create a new Assistant?")):
        setup_new_assistant(config, cache, client)
    else:
        setup_existing_assistant(config, cache, client)


def setup_new_assistant(config: NaviConfig, cache: NaviCache, client: OpenAI) -> None:
    assistant_name: str = click.prompt(
        messaging.make_prompt("Enter Assistant Name"), type=str
    )
    assistant_id = ai.create_assistant(client, assistant_name)

    config["assistant_id"] = assistant_id
    config["thread_id"] = ""
    cache["last_message_id"] = ""


def setup_existing_assistant(
    config: NaviConfig, cache: NaviCache, client: OpenAI
) -> None:
    created_assistant_ids = [(a.id, a.name) for a in ai.get_assistants(client)]
    if created_assistant_ids:
        click.echo(messaging.make_info("Existing Assistants:"))
        for assistant_id, assistant in created_assistant_ids:
            click.echo(messaging.make_info(f"  - {assistant_id}: {assistant}"))
    assistant_id: str = click.prompt(
        messaging.make_prompt("Enter OpenAI Assistant ID"), type=str
    )

    config["assistant_id"] = assistant_id
    config["thread_id"] = ""
    cache["last_message_id"] = ""
