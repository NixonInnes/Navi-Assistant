import itertools
import json
import time
from collections.abc import Iterable
from random import choice

import click
from openai import OpenAI
from openai.types.beta.threads.run import Run
from openai.types.beta.threads.run_submit_tool_outputs_params import ToolOutput
from rich.console import Console
from rich.markdown import Markdown

from .. import ai
from ..commands import Command, load_commands
from ..navi import Navi
from ..style import art, messaging

console = Console()


@click.command()
@click.option(
    "--global", "use_global", is_flag=True, help="Use the global configuration"
)
@click.argument("query", nargs=-1)
def ask(use_global: bool, query: str):
    """Ask your assistant a question."""
    navi = Navi(use_global)
    client = ai.get_client()
    query_string = " ".join(query)

    # Send the user input to the assistant
    send_user_message(navi, client, query_string)

    # Run the assistant
    run_assistant(navi, client)

    # List and display messages in the thread
    display_messages(navi, client)

    navi.save_config()
    navi.save_cache()


def send_user_message(navi: Navi, client: OpenAI, query_string: str):
    """Sends the user's message to the assistant"""
    _ = client.beta.threads.messages.create(
        navi.config["thread_id"], role="user", content=query_string
    )


def run_assistant(navi: Navi, client: OpenAI):
    """Run the assistant and handle any required tool calls"""
    run = client.beta.threads.runs.create(
        thread_id=navi.config["thread_id"], assistant_id=navi.config["assistant_id"]
    )

    for frame in itertools.cycle(art.fairy_frames):
        click.echo("\r" + " " * 50, nl=False)
        click.echo(
            "\r"
            + click.style(f"{{ {run.status:^13} }} ", fg="blue")
            + click.style(frame, fg="magenta"),
            nl=False,
        )

        if run.status == "completed":
            click.echo(
                "\r"
                + click.style(f"{{ {run.status:^12} }} ", fg="blue")
                + click.style(art.styled_fairy, fg="magenta")
                + click.style("/ " + choice(["Hey!", "Listen!"]), fg="yellow")
            )
            return
        elif run.status == "requires_action":
            handle_required_actions(navi, client, run)
        elif run.status in ("cancelling", "cancelled", "failed", "expired"):
            click.echo(messaging.make_error(f"Run status: {run.status}"))
            return
        run = client.beta.threads.runs.retrieve(
            thread_id=navi.config["thread_id"], run_id=run.id
        )
        time.sleep(0.05)


def handle_required_actions(navi: Navi, client: OpenAI, run: Run):
    if run.required_action:
        tool_outputs: list[ToolOutput] = []
        commands: dict[str, Command] = load_commands(navi.tools_dir)

        for tool in run.required_action.submit_tool_outputs.tool_calls:
            command = commands.get(tool.function.name)
            if command:
                kwargs: dict[str, str] = json.loads(tool.function.arguments)
                output = execute_command(command, kwargs)

                if output is not None:
                    tool_outputs.append(ToolOutput(tool_call_id=tool.id, output=output))

        if tool_outputs:
            submit_tool_outputs(client, navi.config["thread_id"], run, tool_outputs)


def execute_command(cmd: Command, args: dict[str, str]):
    try:
        return cmd(**args)
    except Exception as e:
        click.echo(messaging.make_error(f"Error running command: {e!r}"))
        return None


def submit_tool_outputs(
    client: OpenAI, thread_id: str, run: Run, tool_outputs: Iterable[ToolOutput]
):
    try:
        run = client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread_id, run_id=run.id, tool_outputs=tool_outputs
        )
    except Exception as e:
        click.echo(messaging.make_error(f"Error submitting tool outputs: {e!r}"))


def display_messages(navi: Navi, client: OpenAI):
    if navi.cache["last_message_id"]:
        messages = client.beta.threads.messages.list(
            navi.config["thread_id"], after=navi.cache["last_message_id"], order="asc"
        )
    else:
        messages = client.beta.threads.messages.list(
            navi.config["thread_id"], order="asc"
        )

    for message in messages:
        assert message.content[0].type == "text"
        if message.role == "user":
            click.echo(messaging.make_query(message.content[0].text.value))
        else:
            markdown = Markdown(message.content[0].text.value)
            console.print(markdown)
        click.echo()
        navi.cache["last_message_id"] = message.id
