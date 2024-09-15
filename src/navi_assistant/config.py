# src/navi_assistant/config.py

from typing import TypedDict


class NaviConfig(TypedDict):
    """A JSON representation of the Navi Assistant configuration."""
    name: str
    description: str
    instructions: str
    model: str
    assistant_id: str
    thread_id: str

class PartialNaviConfig(NaviConfig, total=False):
    ...


def default_config() -> NaviConfig:
    """Generate a default configuration for the Navi Assistant."""
    return NaviConfig(
        name="Navi",
        description="A CLI personal assistant.",
        instructions="",
        model="gpt-4o-mini",
        assistant_id="",
        thread_id=""
    )

