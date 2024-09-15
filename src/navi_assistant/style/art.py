# src/navi_assistant/style/art.py

import click

_fairy: str = "·.•°•.·.✧ ✦ 🧚 ✦ "

_fairy_motion: str = "·.•°•.·.✧ 🧚"

styled_fairy: str = click.style(_fairy, fg="magenta", bold=True)

fairy_frames: list[str] = [_fairy_motion[-i - 1 :] for i, _ in enumerate(_fairy_motion)]
