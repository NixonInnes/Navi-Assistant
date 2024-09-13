import os
from typing import TypedDict

from . import CONFIG_FILE
from .utils import JsonHandler


class NaviConfig(TypedDict):
    """A JSON representation of the Navi Assistant configuration."""
    name: str
    description: str
    instructions: str
    model: str
    assistant_id: str
    thread_id: str
    available_commands: list[str]

class PartialNaviConfig(NaviConfig, total=False):
    ...


def generate_default_config() -> NaviConfig:
    """Generate a default configuration for the Navi Assistant."""
    return NaviConfig(
        name="Navi",
        description="A CLI personal assistant.",
        instructions="",
        model="gpt-4o-mini",
        api_key="",
        assistant_id="",
        thread_id="",
        available_commands=[],
    )

config_handler = JsonHandler[NaviConfig](
    global_filepath=CONFIG_FILE,
    local_filepath=os.path.join(".navi", "config.json"),
)

