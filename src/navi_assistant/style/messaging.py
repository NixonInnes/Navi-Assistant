# src/navi_assistant/style/messaging.py

import click


def make_header(header: str) -> str:
    return (
        click.style("[ ✦ ", fg="cyan")
        + click.style(header, fg="bright_cyan")
        + click.style(" ✦ ]", fg="cyan")
    )


def make_prompt(prompt: str) -> str:
    return click.style(" ✦ ", fg="cyan") + click.style(prompt, fg="white")


def make_info(info: str) -> str:
    return click.style(" | ", fg="bright_blue") + click.style(info, fg="blue")


def make_warning(warning: str) -> str:
    return click.style(" > ", fg="bright_yellow") + click.style(warning, fg="yellow")


def make_error(error: str) -> str:
    return click.style(" ! ", fg="bright_red") + click.style(error, fg="red")


def make_query(query: str) -> str:
    return click.style(" ?? ", fg="green") + click.style(query, fg="bright_green")


def make_response(response: str) -> str:
    return click.style(response, fg="bright_cyan")
