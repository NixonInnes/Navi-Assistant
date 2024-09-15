import os

# TODO: Add windows support

if xdg_config_home := os.environ.get("XDG_CONFIG_HOME"):
    _config_dir = os.path.join(xdg_config_home, "navi")
else:
    _config_dir = os.path.join(os.path.expanduser("~"), ".config", "navi")

if not os.path.exists(_config_dir):
    os.makedirs(_config_dir, exist_ok=True)


if xdg_cache_home := os.environ.get("XDG_CACHE_HOME"):
    _cache_dir = os.path.join(xdg_cache_home, "navi")
else:
    _cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "navi")

if not os.path.exists(_cache_dir):
    os.makedirs(_cache_dir, exist_ok=True)


GLOBAL_CONFIG_DIR = _config_dir
GLOBAL_CACHE_DIR = _cache_dir
GLOBAL_TOOLS_DIR = os.path.join(_config_dir, "tools")
GLOBAL_CONFIG_FILE = os.path.join(_config_dir, "config.json")
GLOBAL_CACHE_FILE = os.path.join(_cache_dir, "cache.json")
API_KEY_FILE = os.path.join(_config_dir, ".api_key")
