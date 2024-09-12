from openai import OpenAI

from . import commands


def get_client(api_key: str):
    """Return an OpenAI client using the provided API key."""
    return OpenAI(api_key=api_key)


def get_assistants(client: OpenAI):
    """Fetch all assistants from the OpenAI client."""
    assistants = [] 
    
    q = client.beta.assistants.list(limit=20)
    assistants.extend(q.data)
    while q.next_page_info():
        q = q.get_next_page()
        assistants.extend(q.data)
    return assistants


def create_thread(client: OpenAI, assistant_id: str):
    """Create a new thread for the specified assistant."""
    thread = client.beta.threads.create()
    return thread.id


def create_assistant(client: OpenAI, name: str):
    """Create a new assistant with the given name and predefined instructions."""
    assistant = client.beta.assistants.create(
        name=name,
        model="gpt-4o-mini",
        instructions=(
            f"You are a fairy, personal assistant called {name}.\n" +
            "You are used through a command-line interface, so your responses must be in a format suitable to be displayed in a terminal.\n" +
            "Your role is to provide information and assistance to the user.\n" +
            "You have a set of tools which allow you to run commands in the terminal.\n" +
            "When you run a one of your provided tools, you will be given a JSON object containing the stdout, stderr, and return code of the command \n" +
            "in the format: {\"stdout\": \"\", \"stderr\": \"\", \"return_code\": 0}\n"
        ),
        tools=[
            command.definition for command in commands.load_commands().values()
        ]
    )
    return assistant.id
