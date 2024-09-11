import click
import time

from . import config, navi


@click.group()
def cli():
    pass


@cli.command()
def setup():
    click.echo(navi.styled_fairy + navi.make_header("Setup"))
    conf = config.load()

    # Setup API Key
    set_api_key = True
    if existing_key := conf["openai"]["api_key"]:
        click.echo(navi.make_warning(f"API Key already exists in config file: {existing_key}"))
        set_api_key = click.confirm(navi.make_prompt("Do you want to overwrite the existing API Key?"))

    if set_api_key:
        api_key: str = click.prompt(navi.make_prompt("Enter OpenAI API Key"), type=str)
        conf["openai"]["api_key"] = api_key

    client = navi.get_client(conf["openai"]["api_key"])

    # Setup Assistant ID
    set_assistant_id = True
    if existing_id := conf["openai"]["assistant_id"]:
        click.echo(navi.make_warning(f"Assistant ID already exists in config file: {existing_id}"))
        set_assistant_id = click.confirm(navi.make_prompt("Do you want to overwrite the existing Assistant ID?"))

    if set_assistant_id:
        created_assistant_ids = [(a.id, a.name) for a in navi.get_assistants(client)]
        if created_assistant_ids:
            click.echo(navi.make_info("Existing Assistants:"))
            for assistant_id, assistant in created_assistant_ids:
                click.echo(navi.make_info(f"  - {assistant_id}: {assistant}"))
        assistant_id: str = click.prompt(navi.make_prompt("Enter OpenAI Assistant ID"), type=str)
        conf["openai"]["assistant_id"] = assistant_id


    # Create thread
    thread_id = navi.create_thread(client, conf["openai"]["assistant_id"])
    conf["openai"]["thread_id"] = thread_id

    # Save Config
    config.save(conf)

@cli.command()
@click.argument("query", nargs=-1)
def ask(query):
    conf = config.load()
    client = navi.get_client(conf["openai"]["api_key"])
    assistant_id = conf["openai"]["assistant_id"]
    thread_id = conf["openai"]["thread_id"]

    query = " ".join(query)
    
    message = client.beta.threads.messages.create(
        thread_id, 
        role="user",
        content=query)
    
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )

    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id, 
            run_id=run.id)
        time.sleep(1)
        

    messages = client.beta.threads.messages.list(thread_id, limit=1)

    for message in messages:
        assert message.content[0].type == "text"
        print(message.content[0].text.value)


cli.add_command(setup)


if __name__ == "__main__":
    cli()
