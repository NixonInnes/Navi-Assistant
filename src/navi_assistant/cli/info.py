import click

from ..config import config_handler
from ..style import art, messaging



@click.command()
@click.option("--global", "use_global", is_flag=True, help="Use the global configuration")
def info(use_global: bool):
    """Display information about the assistant."""
    click.echo(art.styled_fairy + messaging.make_header("Info"))
    
    is_global, config = config_handler.load(force_global=use_global)
    if is_global:
        click.echo(messaging.make_warning("Global configuration"))
    click.echo(messaging.make_info(f"Name: {config['name']}"))
    click.echo(messaging.make_info(f"Description: {config['description']}"))
    click.echo(messaging.make_info(f"Model: {config['model']}"))
    click.echo(messaging.make_info(f"Assistant ID: {config['assistant_id']}"))
    click.echo(messaging.make_info(f"Thread ID: {config['thread_id']}"))
    click.echo(messaging.make_info("Available Commands:"))
    for command in config["available_commands"]:
        click.echo(messaging.make_info(f"  - {command}"))