import os
from httpx._transports import default
from openai import OpenAI
from openai.types.beta.assistant import Assistant

from . import commands


def get_client(api_key: str) -> OpenAI:
    """Return an OpenAI client using the provided API key."""
    return OpenAI(api_key=api_key)


def get_assistants(client: OpenAI) -> list[Assistant]:
    """Fetch all assistants from the OpenAI client."""
    assistants: list[Assistant] = []

    q = client.beta.assistants.list(limit=20)
    assistants.extend(q.data)
    while q.next_page_info():
        q = q.get_next_page()
        assistants.extend(q.data)
    return assistants


def create_thread(client: OpenAI) -> str:
    """Create a new thread for the specified assistant."""
    thread = client.beta.threads.create()
    return thread.id


def create_assistant(client: OpenAI, name: str) -> str:
    """Create a new assistant with the given name and predefined instructions."""

    # TODO: instructions should be more dynamic (e.g. OS taken into account)
    default_instructions_file: str = os.path.join(os.path.dirname(__file__), "resources", "instructions.txt")
    
    with open(default_instructions_file, "r") as f:
        instructions = f.read()

    # TODO: Fix tools typing
    assistant = client.beta.assistants.create(
        name=name,
        model="gpt-4o-mini",
        instructions=instructions,
        tools=[command.definition for command in commands.load_commands().values()], # pyright: ignore[reportArgumentType]
    )
    return assistant.id
