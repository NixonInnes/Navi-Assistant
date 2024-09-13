import click
import os
from openai import OpenAI

from navi_assistant import CONFIG_DIR, CACHE_DIR, COMMANDS_DIR, CONFIG_FILE, CACHE_FILE, API_KEY_FILE, ai
from navi_assistant.cache import NaviCache, cache_handler, generate_default_cache
from navi_assistant.config import NaviConfig, config_handler, generate_default_config
from navi_assistant.style import art, messaging

def is_setup():
    return all([
        os.path.exists(CONFIG_DIR),
        os.path.exists(COMMANDS_DIR),
        os.path.exists(CONFIG_FILE),
        os.path.exists(CACHE_FILE)
    ])

@click.command()
@click.option("--first-time", is_flag=True, help="Run first-time setup. This will overwrite any existing configuration.")
def install(first_time: bool):
    """Install the assistant configuration."""
    click.echo(art.styled_fairy + messaging.make_header("Installation"))

    if os.path.exists(CONFIG_DIR):
        click.echo(
            messaging.make_warning(
                "It looks like you already have Navi installed."
            ) +
            messaging.make_warning(
                "Running the installer may cause the loss of your current configuration data.\n"
            ) +
            messaging.make_warning(
                 "To modify existing Navi configurations, use `navi config`."
            )
        )
        confirm_warning = click.confirm(
            messaging.make_prompt("Are you sure you want to continue?")
        )

        if not confirm_warning:
            return


    if not is_setup() or first_time:
        first_time_setup()
    setup()


def first_time_setup():
    click.echo(messaging.make_info("Running first-time setup..."))

    os.makedirs(CONFIG_DIR, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)
    os.makedirs(COMMANDS_DIR, exist_ok=True)

    config = generate_default_config()
    config_handler.save(config, force_global=True)

    cache = generate_default_cache()
    cache_handler.save(cache, force_global=True)

    # TODO: Add default commands


def setup():
    _, config = config_handler.load(force_global=True)
    _, cache = cache_handler.load(force_global=True)

    # Setup API Key
    setup_api_key()

    # Create OpenAI Client
    client = ai.get_client()

    # Setup Assistant ID
    setup_assistant(config, cache, client)

    # Create thread
    thread_id = ai.create_thread(client)
    config["thread_id"] = thread_id

    # Save Config
    config_handler.save(config, force_global=True)
    cache_handler.save(cache, force_global=True)


def setup_api_key() -> None:
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, "r") as f:
            existing_key = f.read().strip()
    else:
        existing_key = None
    
    if existing_key:
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
    
    with open(API_KEY_FILE, "w") as f:
        _ = f.write(api_key)


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


