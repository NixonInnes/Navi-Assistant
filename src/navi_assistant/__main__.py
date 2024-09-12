import itertools
import click
import time
from rich.console import Console
from rich.markdown import Markdown 
import json
from random import choice
import tomlkit as tk

from .config import load_config, save_config
from .style import art, messaging
from . import ai, commands

console = Console()


@click.group()
def cli():
    pass


def setup_api_key(config: tk.TOMLDocument) -> None:
    if existing_key := config["openai"]["api_key"]:
        click.echo(messaging.make_warning(f"API Key already exists in config file: {existing_key}"))
        if not click.confirm(messaging.make_prompt("Do you want to overwrite the existing API Key?")):
            return

    api_key: str = click.prompt(messaging.make_prompt("Enter OpenAI API Key"), type=str)
    config["openai"]["api_key"] = api_key


def setup_assistant(config, client) -> None:
    if existing_id := config["openai"]["assistant_id"]:
        click.echo(messaging.make_warning(f"Assistant ID already exists in config file: {existing_id}"))
        if not click.confirm(messaging.make_prompt("Do you want to overwrite the existing Assistant ID?")):
            return

    if click.confirm(messaging.make_prompt("Do you want to create a new Assistant?")):
        setup_new_assistant(config, client)
    else:
        setup_existing_assistant(config, client)
    

def setup_new_assistant(config, client) -> None:
    assistant_name: str = click.prompt(messaging.make_prompt("Enter Assistant Name"), type=str)
    assistant_id = ai.create_assistant(client, assistant_name)

    config["openai"]["assistant_id"] = assistant_id
    config["openai"]["thread_id"] = ""
    config["openai"]["last_message_id"] = ""


def setup_existing_assistant(config, client) -> None:
    created_assistant_ids = [(a.id, a.name) for a in ai.get_assistants(client)]
    if created_assistant_ids:
        click.echo(messaging.make_info("Existing Assistants:"))
        for assistant_id, assistant in created_assistant_ids:
            click.echo(messaging.make_info(f"  - {assistant_id}: {assistant}"))
    assistant_id: str = click.prompt(messaging.make_prompt("Enter OpenAI Assistant ID"), type=str)
    
    config["openai"]["assistant_id"] = assistant_id
    config["openai"]["thread_id"] = ""
    config["openai"]["last_message_id"] = ""

@cli.command()
def setup():
    click.echo(art.styled_fairy + messaging.make_header("Setup"))
    config = load_config()

    # Setup API Key
    setup_api_key(config)

    # Create OpenAI Client
    client = ai.get_client(config["openai"]["api_key"])

    # Setup Assistant ID
    setup_assistant(config, client)
    
    # Create thread
    thread_id = ai.create_thread(client)
    config["openai"]["thread_id"] = thread_id

    # Save Config
    save_config(config)



@cli.command()
@click.argument("query", nargs=-1)
def ask(query):
    """Process the users query and interact with the assistant"""
    config = load_config()
    client = ai.get_client(config["openai"]["api_key"])
    assistant_id = config["openai"]["assistant_id"]
    thread_id = config["openai"]["thread_id"]
    query_string = " ".join(query)

    # Send the user input to the assistant
    send_user_message(client, thread_id, query_string)

    # Run the assistant
    run_assistant(client, thread_id, assistant_id)

    # List and display messages in the thread
    display_messages(client, thread_id, config)


def send_user_message(client, thread_id, query_string):
    """Sends the user's message to the assistant"""
    _ = client.beta.threads.messages.create(
        thread_id, 
        role="user",
        content=query_string)

def run_assistant(client, thread_id, assistant_id):
    """Run the assistant and handle any required tool calls"""
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id)
    
    for frame in itertools.cycle(art.fairy_frames):
        click.echo("\r" + " " * 50 , nl=False)
        click.echo(f"\r" + click.style(f"{{ {run.status:^13} }} ", fg="blue") + click.style(frame, fg="magenta"), nl=False)

        if run.status == "completed":
            click.echo(
                f"\r" + click.style(f"{{ {run.status:^12} }} ", fg="blue") + 
                click.style(art.styled_fairy, fg="magenta") +
                click.style("/ " + choice(["Hey!", "Listen!"]), fg="yellow")
            )
            return
        elif run.status == "requires_action":
            handle_required_actions(client, thread_id, run)
        elif run.status in ("cancelling", "cancelled", "failed", "expired"):
            click.echo(messaging.make_error(f"Run status: {run.status}"))
            return
        run = client.beta.threads.runs.retrieve(
                thread_id=thread_id, 
                run_id=run.id)
        time.sleep(0.05)

def handle_required_actions(client, thread_id, run):
    if run.required_action:

        tool_outputs = []
        cmds = commands.load_commands()

        for tool in run.required_action.submit_tool_outputs.tool_calls:
            cmd = cmds.get(tool.function.name)
            if cmd:
                args = json.loads(tool.function.arguments)
                output = execute_command(cmd, args)

                if output is not None:
                    tool_outputs.append({
                        "tool_call_id": tool.id,
                        "output": output
                    })
        
        if tool_outputs:
            submit_tool_outputs(client, thread_id, run, tool_outputs)

def execute_command(cmd, args):
    try:
        return cmd(**args)
    except Exception as e:
        click.echo(messaging.make_error(f"Error running command: {e!r}"))
        return None


def submit_tool_outputs(client, thread_id, run, tool_outputs):
    try:
        run = client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread_id,
            run_id=run.id,
            tool_outputs=tool_outputs
        )
    except Exception as e:
        click.echo(messaging.make_error(f"Error submitting tool outputs: {e!r}"))


def display_messages(client, thread_id, config):
    if config["openai"]["last_message_id"]:
        messages = client.beta.threads.messages.list(thread_id, after=config["openai"]["last_message_id"], order="asc")
    else:
        messages = client.beta.threads.messages.list(thread_id, order="asc")

    for message in messages:
        assert message.content[0].type == "text"
        if message.role == "user":
            click.echo(messaging.make_query(message.content[0].text.value))
        else:
            markdown = Markdown(message.content[0].text.value)
            console.print(markdown)
        click.echo()
        config["openai"]["last_message_id"] = message.id
    save_config(config)


if __name__ == "__main__":
    cli()
