# src/navi_assistant/ai.py

import os
from openai import OpenAI
from openai.types.beta import AssistantToolParam
from openai.types.beta.assistant import Assistant
from typing import TypedDict

from . import API_KEY_FILE
from .commands import load_commands

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


def create_assistant(client: OpenAI, name: str, model: str, instructions: str, tools_dir: str) -> str:
    # TODO: Fix tools typing
    assistant = client.beta.assistants.create(
        name=name,
        model=model,
        instructions=instructions,
        tools=[tool.definition for tool in load_commands(tools_dir).values()], # pyright: ignore[reportArgumentType]
    )

    return assistant.id

def update_assistant(client: OpenAI, assistant_id: str, name: str, model: str, instructions: str, tools_dir: str) -> None:
    _ = client.beta.assistants.update(
        assistant_id,
        name=name,
        model=model,
        instructions=instructions,
        tools=[tool.definition for tool in load_commands(tools_dir).values()], # pyright: ignore[reportArgumentType]
    )

def create_store(client: OpenAI, name: str) -> str:
    store = client.beta.vector_stores.create(name=name)
    return store.id