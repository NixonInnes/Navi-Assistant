# src/navi_assistant/utils.py

import json
import os


class JsonHandler[T]:
    def __init__(self, filepath: str):
        self.filepath = filepath

    @staticmethod
    def is_local_config() -> bool:
        """Check if there is a local data folder."""
        return os.path.exists(".navi")

    def load(self) -> T:
        """Load the data object type `T` from a json file."""
        with open(self.filepath, "r") as f:
            data_obj: T = json.load(f)

        return data_obj

    def save(self, data_obj: T) -> None:
        """Save the data object type `T` to a json file."""

        with open(self.filepath, "w") as f:
            json.dump(data_obj, f)

