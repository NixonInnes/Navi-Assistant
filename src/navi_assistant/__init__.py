import os

# TODO: Add windows support

if xdg_config_home := os.environ.get("XDG_CONFIG_HOME"):
    _config_dir = os.path.join(xdg_config_home, "navi")
else:
    _config_dir = os.path.join(os.path.expanduser("~"), ".config", "navi")

if not os.path.exists(_config_dir):
    os.makedirs(_config_dir, exist_ok=True)


if xdg_cahce_home := os.environ.get("XDG_CACHE_HOME"):
    _cache_dir = os.path.join(xdg_cahce_home, "navi")
else:
    _cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "navi")

if not os.path.exists(_cache_dir):
    os.makedirs(_cache_dir, exist_ok=True)


CONFIG_FILE = os.path.join(_config_dir, "config.json")
COMMANDS_DIR = os.path.join(_config_dir, "commands")
CACHE_FILE = os.path.join(_cache_dir, "cache.json")
