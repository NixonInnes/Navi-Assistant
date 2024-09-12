import os
import shutil

xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
if xdg_config_home is not None:
    _config_file = os.path.join(xdg_config_home, "navi", "navi.toml")
    _commands_file = os.path.join(xdg_config_home, "navi", "commands.json")
else:
    _config_file = os.path.join(os.path.expanduser("~"), ".config", "navi", "navi.toml")
    _commands_file = os.path.join(
        os.path.expanduser("~"), ".config", "navi", "commands.json"
    )

CONFIG_FILE = _config_file
COMMANDS_FILE = _commands_file


if not os.path.exists(COMMANDS_FILE):
    os.makedirs(os.path.dirname(COMMANDS_FILE), exist_ok=True)
    default = os.path.join(
        os.path.dirname(__file__), "resources", "default_commands.json"
    )
    _ = shutil.copyfile(default, COMMANDS_FILE)
