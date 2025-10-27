import json
from pathlib import Path

DATA_FILE = Path("task.json")
HISTORY_FILE = Path("history.json")


def loadTask() -> list:
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def saveTask(task: list) -> list:
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(task, f, indent=2, ensure_ascii=False)


def loadHistory() -> list:
    if not HISTORY_FILE.exists():
        return []
    with HISTORY_FILE.open('r', encoding="utf-8") as a:
        try:
            return json.load(a)
        except json.JSONDecodeError:
            return []

def saveHistory(history: list) -> None:
    with HISTORY_FILE.open("w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
