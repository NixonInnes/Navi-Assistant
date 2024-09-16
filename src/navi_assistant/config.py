# src/navi_assistant/config.py

from typing import TypedDict


class NaviConfig(TypedDict):
    """A JSON representation of the Navi Assistant configuration."""

    name: str
    description: str
    instructions: str
    model: str
    store_id: str
    assistant_id: str
    thread_id: str
    store_folders: list[str]
    store_file_extensions: list[str]


class PartialNaviConfig(NaviConfig, total=False): ...


def default_config() -> NaviConfig:
    """Generate a default configuration for the Navi Assistant."""
    return NaviConfig(
        name="Navi",
        description="A CLI personal assistant.",
        instructions="",
        model="gpt-4o-mini",
        store_id="",
        assistant_id="",
        thread_id="",
        store_folders=[],
        store_file_extensions=[],
    )
