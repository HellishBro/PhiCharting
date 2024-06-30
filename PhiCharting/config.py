import json5
from tkinter import messagebox
from pathlib import Path
import sys
from os import path

class Config:
    INSTANCE: 'Config' = None

    @classmethod
    def instance(cls) -> 'Config':
        if Config.INSTANCE:
            return Config.INSTANCE
        else:
            Config.INSTANCE = Config()
            return Config.INSTANCE

    def __init__(self, location="config.json5"):
        if Config.INSTANCE is not None:
            raise ValueError("Config class initialized more than once.")

        location = Path(path.abspath(location))
        try:
            with open(location) as f:
                self.data = json5.loads(f.read())
            self.location = location
        except FileNotFoundError:
            messagebox.showerror("Config File Not Found!", f"No config file found at '{location}'! Is it named '{location.name}'?")
            sys.exit(-1)
        except ValueError:
            messagebox.showerror("JSON5 Decode Error!", f"Unable to parse config file '{location}'! Is it valid JSON/JSON5?")
            sys.exit(-1)

    def get(self, key: str, default=None):
        if key in self.data:
            return self.data[key]
        else:
            return self.set(key, default)

    def set(self, key: str, value):
        self.data[key] = value
        return value

    def save(self):
        try:
            with open(self.location, "w") as f:
                f.write(json5.dumps(self.data))
        except FileNotFoundError:
            messagebox.showerror("Config File Not Found!", f"No config file found at '{self.location}'! Is it named '{self.location.name}'?")
            sys.exit(-1)
