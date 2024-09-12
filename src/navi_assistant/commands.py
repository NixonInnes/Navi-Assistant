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
        command = self.command.format(**kwargs)

        result = subprocess.run(command, text=True, capture_output=True, shell=True)
        return json.dumps({
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        })