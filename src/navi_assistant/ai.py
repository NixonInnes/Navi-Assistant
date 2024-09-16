# src/navi_assistant/ai.py

import os
from openai import OpenAI
from openai.types.beta import AssistantToolParam
from openai.types.beta.assistant import Assistant
from pathlib import Path
from typing import TypedDict

from openai.types.beta.vector_stores.vector_store_file import VectorStoreFile

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


def create_assistant(client: OpenAI, name: str, model: str, instructions: str, tools_dir: str) -> tuple[str, str]:
    # TODO: Fix tools typing
    store_id = create_store(client, name+"-store")
    tools= [{"type": "file_search"}] + [tool.definition for tool in load_commands(tools_dir).values()], # pyright: ignore[reportArgumentType]
    print(tools)
    assistant = client.beta.assistants.create(
        name=name,
        model=model,
        instructions=instructions,
        tools=
            [{"type": "file_search"}] +
            [tool.definition for tool in load_commands(tools_dir).values()], # pyright: ignore[reportArgumentType]
        tool_resources={"file_search": {"vector_store_ids": [store_id]}},
    )

    return assistant.id, store_id

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



def get_store_files(dirs: list[str], extensions: list[str]) -> list[str]:
    files: list[str] = []

    cwd = Path.cwd()

    for d in dirs:
        for ext in extensions:
            files.extend([str(p) for p in (cwd / d).rglob(f"*.{ext}")])

    return files


def upload_file(client: OpenAI, store_id: str, file: str) -> VectorStoreFile:
    store_file = client.files.create(
        file=open(file, "rb"),
        purpose="assistants",
    )
    return client.beta.vector_stores.files.create(
        vector_store_id=store_id, 
        file_id=store_file.id)

def delete_file(client: OpenAI, store_id: str, file_id: str) -> None:
    _ = client.beta.vector_stores.files.delete(
        vector_store_id=store_id,
        file_id=file_id
    )
    _ = client.files.delete(file_id)

def list_store_files(client: OpenAI, store_id: str) -> list[VectorStoreFile]:
    files: list[VectorStoreFile] = []

    q = client.beta.vector_stores.files.list(store_id, limit=20)
    files.extend(q.data)
    while q.next_page_info():
        q = q.get_next_page()
        files.extend(q.data)
    return files