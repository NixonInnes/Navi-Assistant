import click

_fairy = "·.•°•.·.✧ ✦ 🧚 ✦ "

_fairy_motion = "·.•°•.·.✧ 🧚"

styled_fairy = click.style(_fairy, fg="magenta", bold=True)

fairy_frames = [_fairy_motion[-i-1:] for i,_ in enumerate(_fairy_motion)]