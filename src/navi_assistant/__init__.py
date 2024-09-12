import os
import shutil


if xdg_config_home:=os.environ.get("XDG_CONFIG_HOME") is not None:
    CONFIG_FILE = os.path.join(xdg_config_home, "navi", "navi.toml")
    COMMANDS_FILE = os.path.join(xdg_config_home, "navi", "commands.json")
else:
    CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".config", "navi", "navi.toml")
    COMMANDS_FILE = os.path.join(os.path.expanduser("~"), ".config", "navi", "commands.json")


if not os.path.exists(COMMANDS_FILE):
    os.makedirs(os.path.dirname(COMMANDS_FILE), exist_ok=True)
    default = os.path.join(os.path.dirname(__file__), "resources", "default_commands.json")
    shutil.copyfile(default, COMMANDS_FILE)

