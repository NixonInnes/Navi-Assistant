# src/navi_assistant/cache.py

from typing import TypedDict


class NaviCache(TypedDict):
    """A JSON representation of the Navi Assistant cache."""

    last_message_id: str
    last_query: str
    last_response: str


def default_cache() -> NaviCache:
    """Generate a default cache for the Navi Assistant."""
    return NaviCache(
        last_message_id="",
        last_query="",
        last_response=""
    )
