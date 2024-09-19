# src/navi_assistant/cache.py

from typing import TypedDict


class NaviCacheStoreFile(TypedDict):
    """A JSON representation of a file in the Navi Assistant cache."""

    id: str
    uploaded: float


class NaviCache(TypedDict):
    """A JSON representation of the Navi Assistant cache."""

    last_message_id: str
    last_query: str
    last_response: str
    store_files: dict[str, NaviCacheStoreFile]


def default_cache() -> NaviCache:
    """Generate a default cache for the Navi Assistant."""
    return NaviCache(
        last_message_id="", last_query="", last_response="", store_files={}
    )
