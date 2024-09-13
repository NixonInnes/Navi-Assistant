import os
from openai import OpenAI
from openai.types.beta import AssistantToolParam
from openai.types.beta.assistant import Assistant
from typing import TypedDict

from . import commands, API_KEY_FILE

class AssistantSpec(TypedDict):
    name: str | None
    model: str
    instructions: str
    tools: list[AssistantToolParam]


def get_api_key() -> str:
    """Return the API key from the configuration file."""
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, "r") as f:
            return f.read().strip()
    raise FileNotFoundError("API key file not found.")


def get_client() -> OpenAI:
    """Return an OpenAI client using the provided API key."""
    return OpenAI(api_key=get_api_key())


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


def build_assistant(name: str | None = None) -> AssistantSpec:
    # TODO: instructions should be more dynamic (e.g. OS taken into account)
    default_instructions_file: str = os.path.join(os.path.dirname(__file__), "resources", "instructions.txt")
    
    with open(default_instructions_file, "r") as f:
        instructions = f.read()

    # TODO: Fix tools typing
    assistant = AssistantSpec(
        name=name,
        model="gpt-4o-mini",
        instructions=instructions,
        tools=[command.definition for command in commands.load_commands().values()], # pyright: ignore[reportArgumentType]
    )
    return assistant

def create_assistant(client: OpenAI, name: str) -> str:
    assistant = client.beta.assistants.create(
        **build_assistant(name)
    )
    return assistant.id

def update_assistant(client: OpenAI, assistant_id: str) -> None:
    _ = client.beta.assistants.update(
        assistant_id,
        **build_assistant()
    )