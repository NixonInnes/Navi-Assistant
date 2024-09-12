import tomlkit as tk


from . import CONFIG_FILE


def generate_default_config():
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


def load_config() -> tk.TOMLDocument:
    with open(CONFIG_FILE, "r") as f:
        config = tk.load(f)

    return config


def save_config(doc: tk.TOMLDocument) -> None:
    with open(CONFIG_FILE, "w") as f:
        tk.dump(doc, f)