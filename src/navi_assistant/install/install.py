import click
import os

from navi_assistant import GLOBAL_CONFIG_DIR, GLOBAL_CACHE_DIR, GLOBAL_TOOLS_DIR, GLOBAL_CONFIG_FILE, GLOBAL_CACHE_FILE, API_KEY_FILE, ai
from navi_assistant.navi import Navi
from navi_assistant.style import art, messaging
from navi_assistant.cli.init import setup_assistant

def is_setup():
    return all([
        os.path.exists(GLOBAL_CONFIG_DIR),
        os.path.exists(GLOBAL_TOOLS_DIR),
        os.path.exists(GLOBAL_CONFIG_FILE),
        os.path.exists(GLOBAL_CACHE_FILE)
    ])

@click.command()
@click.option("--first-time", is_flag=True, help="Run first-time setup. This will overwrite any existing configuration.")
def install(first_time: bool):
    """Install the assistant configuration."""
    click.echo(art.styled_fairy + messaging.make_header("Installation"))

    if os.path.exists(GLOBAL_CONFIG_DIR):
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

    os.makedirs(GLOBAL_CONFIG_DIR, exist_ok=True)
    os.makedirs(GLOBAL_CACHE_DIR, exist_ok=True)
    os.makedirs(GLOBAL_TOOLS_DIR, exist_ok=True)

    navi = Navi(is_global=True, load_defaults=True)
    navi.save_config()
    navi.save_cache()


def setup():
    navi = Navi(is_global=True)

    # Setup API Key
    setup_api_key()

    # Create OpenAI Client
    client = ai.get_client()

    # Setup Assistant ID
    setup_assistant(navi, client)

    # Create thread
    thread_id = ai.create_thread(client)
    navi.config["thread_id"] = thread_id

    # Save Config
    navi.save_config()
    navi.save_cache()


def setup_api_key() -> None:
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, "r") as f:
            existing_key = f.read().strip()
    else:
        existing_key = None
    
    if existing_key:
        click.echo(
            messaging.make_warning(
                f"An API Key already exists in: {API_KEY_FILE}"
            )
        )
        if not click.confirm(
            messaging.make_prompt("Do you want to overwrite the existing API Key?")
        ):
            return

    api_key: str = click.prompt(messaging.make_prompt("Enter OpenAI API Key"), type=str)
    
    with open(API_KEY_FILE, "w") as f:
        _ = f.write(api_key)



