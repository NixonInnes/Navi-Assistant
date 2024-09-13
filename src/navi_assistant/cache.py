import os

from typing import TypedDict

from . import CACHE_FILE
from .utils import JsonHandler


class NaviCache(TypedDict):
    """A JSON representation of the Navi Assistant cache."""

    last_message_id: str
    last_query: str
    last_response: str


def generate_default_cache() -> NaviCache:
    """Generate a default cache for the Navi Assistant."""
    return NaviCache(
        last_message_id="",
        last_query="",
        last_response=""
    )

cache_handler = JsonHandler[NaviCache](
    global_filepath=CACHE_FILE,
    local_filepath=os.path.join(".navi", "cache.json")
)
