import json
import os
from typing import TypedDict

from . import CONFIG_FILE


class NaviConfig(TypedDict):
    """A JSON representation of the Navi Assistant configuration."""

    api_key: str
    assistant_id: str
    thread_id: str
    available_commands: list[str]


def generate_default_config() -> NaviConfig:
    """Generate a default configuration for the Navi Assistant."""
    return NaviConfig(
        api_key="",
        assistant_id="",
        thread_id="",
        available_commands=[],
    )


def load_config() -> NaviConfig:
    """Load the configuration from the config file."""
    if not os.path.exists(CONFIG_FILE):
        config = generate_default_config()
        save_config(config)
    else:
        with open(CONFIG_FILE, "r") as f:
            config: NaviConfig = json.load(f)

    return config


def save_config(config: NaviConfig) -> None:
    """Save the configuration document to the config file."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)
