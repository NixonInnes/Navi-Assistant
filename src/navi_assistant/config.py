import os
import tomlkit as tk


if xdg_config_home:=os.environ.get("XDG_CONFIG_HOME") is not None:
    CONFIG_FILE = os.path.join(xdg_config_home, "navi", "navi.toml")
else:
    CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".config", "navi", "navi.toml")


def generate_default_config():
    navi = tk.table()
    openai = (
        tk.table()
        .add("api_key", "")
        .add("assistant_id", "")
        .add("thread_id", "")
    )

    doc = (
        tk.document()
        .add(tk.comment("Navi Assistant Configuration"))
        .add(tk.nl())
        .add("navi", navi)
        .add("openai", openai)
    )

    return doc


def load() -> tk.TOMLDocument:
    if not os.path.exists(CONFIG_FILE):
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        save(generate_default_config())

    with open(CONFIG_FILE, "r") as f:
        config = tk.load(f)

    return config


def save(doc: tk.TOMLDocument) -> None:
    with open(CONFIG_FILE, "w") as f:
        tk.dump(doc, f)