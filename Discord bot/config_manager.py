import json
import os

CONFIG_FILE = "config.json"

class ConfigManager:
    def __init__(self, file_path=CONFIG_FILE):
        self.file_path = file_path
        self.config = {}
        self.load()

    def load(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Config file '{self.file_path}' not found.")
        with open(self.file_path, "r") as f:
            self.config = json.load(f)

    def save(self):
        with open(self.file_path, "w") as f:
            json.dump(self.config, f, indent=2)

    def get(self, key_path, default=None):
        keys = key_path.split(".")
        d = self.config
        try:
            for key in keys:
                d = d[key]
            return d
        except (KeyError, TypeError):
            return default

    def set(self, key_path, value):
        keys = key_path.split(".")
        d = self.config
        for key in keys[:-1]:
            d = d.setdefault(key, {})
        d[keys[-1]] = value
        self.save()

    def toggle(self, key_path):
        keys = key_path.split(".")
        d = self.config
        for key in keys[:-1]:
            d = d[key]
        d[keys[-1]] = not d[keys[-1]]
        self.save()
        return d[keys[-1]]

config = ConfigManager()