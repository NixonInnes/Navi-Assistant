import subprocess
import json
import logging

from . import COMMANDS_FILE

def load_commands() -> dict[str, "Command"]:
    """Load commands from the commands file and return a dictionary of Command objects."""
    with open(COMMANDS_FILE, "r") as f:
        commands: dict[str, str | dict[str, str]] = json.load(f)

    return {
        name: Command(name, command["command"], command["input"], command["definition"]) 
        for name, command in commands.items()
    }

class Command:
    def __init__(self, name: str, command: str, input: str | None, definition: dict[str, dict]):
        self._logger = logging.getLogger(f"Command.{name}")
        definition["function"]["name"] = name

        self.name = name
        self.command = command
        self.input = input
        self.definition = definition

    def __call__(self, **kwargs: str) -> str:
        """Run the command with the given kwargs and return the result in JSON format."""
        command = self.command.format(**kwargs)

        if self.input:
            input = self.input.format(**kwargs)
            self._logger.info(f"{self.name}: command:{self.command} input:{input}")
            result = subprocess.run(command, input=input, text=True, capture_output=True, shell=True)
        else:
            self._logger.info(f"{self.name}: command:{self.command}")
            result = subprocess.run(command, text=True, capture_output=True, shell=True)
        return json.dumps({
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        })