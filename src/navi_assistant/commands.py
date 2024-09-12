import json
import logging
import subprocess
from typing import Literal, Self, TypeAlias, TypedDict

from openai.types.beta.function_tool import FunctionTool
from openai.types.shared.function_definition import FunctionDefinition
from openai.types.shared.function_parameters import FunctionParameters

from . import COMMANDS_FILE


class PartialFunctionDefinition(TypedDict):
    """A partial definition of the OpenAI FunctionDefinition object.
    The definition is missing "name" as we set that as a key in our commands.json.
    """

    description: str
    parameters: FunctionParameters
    strict: bool


class PartialFunctionTool(TypedDict):
    """A partial definition of the OpenAI FunctionTool object.
    Just replaces the "function" field with a PartialFunctionDefinition.
    """

    type: Literal["function"]
    function: PartialFunctionDefinition


class JSONCommand(TypedDict):
    """A JSON representation of a Command object."""

    command: str
    input: str | None
    definition: PartialFunctionTool


JSONCommandContainer: TypeAlias = dict[str, JSONCommand]


def load_commands() -> dict[str, "Command"]:
    """Load commands from the commands file and return a dictionary of Command objects."""
    with open(COMMANDS_FILE, "r") as f:
        dic: JSONCommandContainer = json.load(f)
        commands = {name: JSONCommand(**command) for name, command in dic.items()}

    return {
        name: Command.from_json(name, command) for name, command in commands.items()
    }


class Command:
    name: str
    command: str
    input: str | None
    definition: FunctionTool

    def __init__(
        self, name: str, command: str, input: str | None, definition: FunctionTool
    ):
        self._logger = logging.getLogger(f"Command.{name}")
        self.name = name
        self.command = command
        self.input = input
        self.definition = definition

    @classmethod
    def from_json(cls, name: str, json_object: JSONCommand) -> Self:
        """Create a new Command object from a JSON object."""
        return cls(
            name=name,
            command=json_object["command"],
            input=json_object["input"],
            definition=FunctionTool(
                type=json_object["definition"]["type"],
                function=FunctionDefinition(
                    name=name, **json_object["definition"]["function"]
                ),
            ),
        )

    def __call__(self, **kwargs: str) -> str:
        """Run the command with the given kwargs and return the result in JSON format."""
        command = self.command.format(**kwargs)

        if self.input:
            input = self.input.format(**kwargs)
            self._logger.info(f"{self.name}: command:{self.command} input:{input}")
            result = subprocess.run(
                command, input=input, text=True, capture_output=True, shell=True
            )
        else:
            self._logger.info(f"{self.name}: command:{self.command}")
            result = subprocess.run(command, text=True, capture_output=True, shell=True)
        return json.dumps(
            {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }
        )
