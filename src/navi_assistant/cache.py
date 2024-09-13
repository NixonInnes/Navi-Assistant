import json
import os

from typing import TypedDict

from . import CACHE_FILE


class NaviCache(TypedDict):
    """A JSON representation of the Navi Assistant cache."""

    last_message_id: str


def generate_default_cache() -> NaviCache:
    """Generate a default cache for the Navi Assistant."""
    return NaviCache(last_message_id="")


def load_cache() -> NaviCache:
    """Load the cache from the cache file."""
    if not os.path.exists(CACHE_FILE):
        cache = generate_default_cache()
        save_cache(cache)
    else:
        with open(CACHE_FILE, "r") as f:
            cache: NaviCache = json.load(f)

    return cache


def save_cache(cache: NaviCache) -> None:
    """Save the cache document to the cache file."""
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)