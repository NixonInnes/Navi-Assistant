from openai import OpenAI

from . import commands


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


def create_assistant(client: OpenAI, name: str):
    assistant = client.beta.assistants.create(
        name=name,
        model="gpt-4o-mini",
        instructions=(
            f"You are a fairy, personal assistant called {name}.\n" +
            "You are used through a command-line interface, so your responses must be in a format suitable to be displayed in a terminal.\n" +
            "Your role is to provide information and assistance to the user.\n" +
            "You have a set of tools which allow you to get information about the users system.\n"
        ),
        tools=[
            command.definition for command in commands.load_commands().values()
        ]
    )
    return assistant.id
