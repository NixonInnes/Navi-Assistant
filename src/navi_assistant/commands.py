import os 
import subprocess
import json
import logging

from . import COMMANDS_FILE

def load_commands() -> dict:
    with open(COMMANDS_FILE, "r") as f:
        commands = json.load(f)

    return {
        name: Command(name, command["command"], command["definition"]) for name, command in commands.items()
    }

class Command:
    def __init__(self, name: str, command: str, definition: dict):
        self._logger = logging.getLogger(f"Command.{name}")
        definition["function"]["name"] = name

        self.name = name
        self.command = command
        self.definition = definition

    def __call__(self, **kwargs):
        self._logger.info(f"Running command: {self.name}")
        command = self.command.format(**kwargs).split(" ")

        result = subprocess.run(command, text=True, capture_output=True)
        return json.dumps({
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        })


read_file_func = {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": (
            "Returns the contents of a file. \n" + 
            "This function takes a single parameter, 'file', which is the path to the file to read."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "file": {
                    "type": "string",
                    "description": "The path to the file to read.",
                }
            },
            "required": ["file"],
            "additionalProperties": False,
        },
        "strict": True,
    }
}


def read_file(file: str) -> str:
    print(f"Trying to read file: {file}")
    if not os.path.exists(file):
        print(f"File not found: {file}")
        return f"File not found: {file}"
    else:
        print(f"Reading file: {file}")
    with open(file, "r") as f:
        return f.read()