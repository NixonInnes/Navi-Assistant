# src/navi_assistant/cli/init.py

import os

import click
from openai import OpenAI

from .. import ai
from ..navi import Navi
from ..style import art, messaging


@click.command()
def init():
    """Create a new local assistant."""
    click.echo(art.styled_fairy + messaging.make_header("Initialising"))

    navi = Navi(is_global=False, load_defaults=True)
    os.makedirs(navi.config_dir, exist_ok=True)
    os.makedirs(navi.cache_dir, exist_ok=True)
    os.makedirs(navi.tools_dir, exist_ok=True)

    if not os.path.exists(navi.config_file):
        click.echo(messaging.make_info("Creating new assistant..."))
        navi.save_config()
    else:
        click.echo(messaging.make_warning("A local asssistant already exists."))
        navi.load_config()

    if not os.path.exists(navi.cache_file):
        navi.save_cache()
    else:
        navi.load_cache()

    client = ai.get_client()

    navi.config["thread_id"] = ai.create_thread(client)

    setup_assistant(navi, client)

    navi.save_config()
    navi.save_cache()


def setup_assistant(navi: Navi, client: OpenAI) -> None:
    if existing_id := navi.config["assistant_id"]:
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
        setup_new_assistant(navi, client)
    else:
        setup_existing_assistant(navi, client)


def setup_new_assistant(navi: Navi, client: OpenAI) -> None:
    name: str = click.prompt(messaging.make_prompt("Enter Assistant Name"), type=str)
    description: str = click.prompt(
        messaging.make_prompt("Enter Assistant Description"), type=str
    )
    instructions: str = click.prompt(
        messaging.make_prompt("Enter Assistant Instructions"), type=str
    )
    model: str = click.prompt(messaging.make_prompt("Enter Assistant Model"), type=str)

    navi.config["name"] = name
    navi.config["description"] = description
    navi.config["instructions"] = instructions
    navi.config["model"] = model
    navi.config["assistant_id"], navi.config["store_id"] = ai.create_assistant(
        client,
        name,
        model,
        instructions,
        navi.tools_dir,
    )
    navi.config["thread_id"] = ai.create_thread(client)
    navi.cache["last_message_id"] = ""


def setup_existing_assistant(navi: Navi, client: OpenAI) -> None:
    created_assistant_ids = [(a.id, a.name) for a in ai.get_assistants(client)]
    if created_assistant_ids:
        click.echo(messaging.make_info("Existing Assistants:"))
        for assistant_id, assistant in created_assistant_ids:
            click.echo(messaging.make_info(f"  - {assistant_id}: {assistant}"))
    assistant_id: str = click.prompt(
        messaging.make_prompt("Enter OpenAI Assistant ID"), type=str
    )

    navi.config["assistant_id"] = assistant_id
    navi.config["thread_id"] = ""
    navi.cache["last_message_id"] = ""
