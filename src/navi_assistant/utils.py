import json
import os


class JsonHandler[T]:
    def __init__(self, global_filepath: str, local_filepath: str):
        self.global_filepath = global_filepath
        self.local_filepath = local_filepath

    @staticmethod
    def is_local_config() -> bool:
        """Check if there is a local data folder."""
        return os.path.exists(".navi")
    
    def load(self, force_global: bool = False) -> tuple[bool, T]:
        """Load the data object type `T` from either a local or global json file."""
        
        if not force_global and self.is_local_config():
            is_global = False
            json_file = self.local_filepath
        else:
            is_global = True
            json_file = self.global_filepath
        
        try:
            with open(json_file, "r") as f:
                data_obj: T = json.load(f)
        except FileNotFoundError:
            if is_global:
                raise FileNotFoundError(f"No such file: '{json_file}'. Please make sure Navi is correctly installed.")
            raise FileNotFoundError(f"No such file: '{json_file}'. Use `navi init` to create the required local configuration files.")
        
        return is_global, data_obj

    def save(self, data_obj: T, force_global: bool = False) -> None:
        """Save the data object type `T` to either a local or global json file."""

        if not force_global and self.is_local_config():
            json_file = self.local_filepath
        else:
            json_file = self.global_filepath

        with open(json_file, "w") as f:
            json.dump(data_obj, f)