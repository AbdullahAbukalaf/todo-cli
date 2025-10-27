import json
from pathlib import Path

DATA_FILE = Path("task.json")

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