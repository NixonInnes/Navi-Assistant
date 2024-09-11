import sys
import click
import time
from openai import OpenAI
import itertools


fairy = "·.•°•.·.✧ ✦ 🧚 ✦ "

styled_fairy = click.style(fairy, fg="magenta", bold=True)


def make_header(header: str):
    return (
        click.style("[ ✦ ", fg="cyan")
        + click.style(header, fg="bright_cyan")
        + click.style(" ✦ ]", fg="cyan")
    )


def make_prompt(prompt: str):
    return click.style(" ✦ ", fg="cyan") + click.style(prompt, fg="white")

def make_info(info: str):
    return click.style(" | ", fg="bright_blue") + click.style(info, fg="blue")

def make_warning(warning: str):
    return click.style(" > ", fg="bright_yellow") + click.style(warning, fg="yellow")

def get_client(api_key: str):
    return OpenAI(api_key=api_key)

def get_assistants(client: OpenAI):
    assistants = [] 
    
    q = client.beta.assistants.list(limit=20)
    assistants.extend(q.data)
    while q.next_page_info():
        q = q.get_next_page()
        assistants.extend(q.data)
    return assistants

def create_thread(client: OpenAI, assistant_id: str):
    thread = client.beta.threads.create()
    return thread.id

frames = [
    click.style("🧚 ", fg="magenta"),
    click.style("· 🧚 ", fg="magenta"),
    click.style("·. 🧚 ", fg="magenta"),
    click.style("·.• 🧚 ", fg="magenta"),
    click.style("·.•° 🧚 ", fg="magenta"),
    click.style("·.•°• 🧚 ", fg="magenta"),
    click.style("·.•°•. 🧚 ", fg="magenta"),
    click.style("·.•°•.· 🧚 ", fg="magenta"),
    click.style("·.•°•.·. 🧚 ", fg="magenta"),
    click.style("·.•°•.·.✧ 🧚 ", fg="magenta"),
]

def animated_loading(duration):
    """Display a loading animation for a specified duration."""
    for frame in itertools.cycle(frames):
        # Print the frame, using '\r' to overwrite the line
        sys.stdout.write('\r' + ' ' * 50 + '\r')
        sys.stdout.write(frame)
        sys.stdout.flush()
        time.sleep(0.2)  # Control the speed of the animation

        # Exit after the specified duration
        if duration <= 0:
            break
        duration -= 0.2

def wait_on_run(run, thread):
    while run.status != "completed":
        run = thread.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id)
        time.sleep(0.1)
    return run
