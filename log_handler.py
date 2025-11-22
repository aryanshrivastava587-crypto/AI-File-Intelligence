"""
log_handler.py
Simple JSON log handler that appends entries to a log file.
"""
import json
from pathlib import Path

class LogHandler:
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        if not self.filepath.exists():
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump([], f)

    def append(self, entry):
        data = []
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = []
        data.append(entry)
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
