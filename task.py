def createTask(task_id: int, task_title: str, task_priority : str = "Medium"):
    return {
        "id": task_id,
        "title": task_title,
        "priority" : task_priority,
        "done": False
    }


def markAsDone(task: dict) -> None:
    task["done"] = True



    