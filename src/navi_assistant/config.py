import os
import tomlkit as tk
from tomlkit.container import Container

from . import CONFIG_FILE


def generate_default_config() -> Container:
    """Generate a default configuration for the Navi Assistant."""
    navi = tk.table()
    openai = (
        tk.table()
        .add("api_key", "")
        .add("assistant_id", "")
        .add("thread_id", "")
        .add("last_message_id", "")
    )

    doc = (
        tk.document()
        .add(tk.comment("Navi Assistant Configuration"))
        .add(tk.nl())
        .add("navi", navi)
        .add("openai", openai)
        
    )

    return doc


def load_config() -> Container:
    """Load the configuration from the config file."""
    if not os.path.exists(CONFIG_FILE):
        config = generate_default_config()
        save_config(config)
    else:
        with open(CONFIG_FILE, "r") as f:
            config = tk.load(f)

    return config


def save_config(doc: Container) -> None:
    """Save the configuration document to the config file."""
    with open(CONFIG_FILE, "w") as f:
        tk.dump(doc, f)


if not os.path.exists(CONFIG_FILE):
    doc = generate_default_config()
    save_config(doc)
