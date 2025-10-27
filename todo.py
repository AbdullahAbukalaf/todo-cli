from task import createTask, markAsDone
from storage import saveTask, loadTask, loadHistory, saveHistory
import sys
USAGE = """
To-Do CLI
Usage:
  python todo.py add "task title"     -> add new task
  python todo.py list                 -> list all tasks
  python todo.py done <task_id>       -> mark a task as done
  python todo.py delete <task_id>     -> delete a task
  python todo.py edit <task_id> "new title"     -> edit task title
"""

# Add function


def cmd_add(title: str, priority: str):
    tasks = loadTask()
    if priority == "--high":
        priority = "High"
    elif priority == "--low":
        priority = "Low"
    else:
        priority = "Medium"
    next_id = (max([t["id"] for t in tasks]) + 1) if tasks else 1
    new_task = createTask(next_id, title, priority)
    tasks.append(new_task)
    saveTask(tasks)
    print(f'✅ Added task #{next_id}: "{title}"')

# Fetch the data


def cmd_list(tasktatus: bool = False):
    tasks = loadTask()
    if not tasks:
        print("No tasks yet.")
        return
    if tasktatus:
        pendingTasks = [t for t in tasks if t["done"] is False]
        if not pendingTasks:
            print("No pending tasks. 🎉")
            return
    else:
        pendingTasks = tasks

    print("Your tasks:\n")
    for t in pendingTasks:
            status = "✔" if t["done"] else "✖"
            print(f'{t["id"]:>3}. [{status}] [{t["priority"]}] {t["title"]}')
    print()

# Mark task ans done


def cmd_done(taskId: str):
    tasks = loadTask()
    try:
        task_id = int(taskId)
    except ValueError:
        print("Task ID must be a number.")
        return

    for t in tasks:
        if t["id"] == task_id:
            if t["done"]:
                print(f'{t["id"]} is already mark as done.')
            else:
                markAsDone(t)
                saveTask(tasks)
                print(f"✅ Marked task #{task_id} as done.")
            return

    print(f"Task #{task_id} not found.")

# edit task title


def cmd_edit(taskId: str, newTitle: str):
    tasks = loadTask()
    try:
        task_id = int(taskId)
    except ValueError:
        print("Task Id must be a number.")
        return

    for t in tasks:
        if t["id"] == task_id:
            if t["title"] == newTitle:
                print("You entered the same title, try changing it to a new one.")
                return
            t["title"] = newTitle
            print(f'#{t["id"]} task title updated successfully.')
            saveTask(tasks)
            return

    print(f"Task #{task_id} not found.")

# delete a task


def cmd_delete(taskId: str):
    tasks = loadTask()
    try:
        task_id = int(taskId)
    except ValueError:
        print("task ID must be a number.")
        return

    # find the task we're about to delete
    task_to_delete = {}
    for t in tasks:
        if t["id"] == task_id:
            task_to_delete = t
            break

    if not task_to_delete:
        print(f"Task #{task_id} not found")
        return

    # save undo info BEFORE deleting
    history = loadHistory()
    history.append({
        "action": "restore_task",
        "task": task_to_delete
    })
    saveHistory(history)

    # now actually delete it
    new_tasks = [t for t in tasks if t["id"] != task_id]
    saveTask(new_tasks)
    print(f"🗑 Deleted task #{task_id}.")
    print(history)

# clear tasks


def cmd_clear():
    saveTask([])
    print("All tasks cleared.")


def cmd_undo():
    history = loadHistory()
    if not history:
        print("Nothing to undo.")
        return
    print(history)
    last = history.pop()  # get the last action

    action_type = last["action"]

    tasks = loadTask()

    # 1. undo delete (restore one task)
    if action_type == "restore_task":
        restored_task = last["task"]
        tasks.append(restored_task)
        tasks.sort(key=lambda x: x["id"])
        saveTask(tasks)
        print(f'Restored task #{restored_task["id"]}: "{restored_task["title"]}"')
    else:
        print("Undo action type not recognized.")
    
    saveHistory(history)
        
#main function
def main():
    if len(sys.argv) < 2:
        print(USAGE)
        return
    
    command = sys.argv[1].lower()
    
    if command == "add":
        if len(sys.argv) < 3:
            print("Please provide a task title.\nExample:\n  python todo.py add \"Buy milk\"")
            return
        args_after_add = sys.argv[2:]
        priority_flag = "Medium"
        last_arg = args_after_add[-1]
        if last_arg in ["--low", "--high"]:
            priority_flag = last_arg
            args_after_add = args_after_add[:-1]
        title = " ".join(args_after_add)
        cmd_add(title,priority_flag)
        
    elif command == "list":
       show_pending = ("--pending" in sys.argv[2:])
       cmd_list(show_pending)
        
    elif command == "done":
        if len(sys.argv) < 3:
            print("Please provide the task ID to mark done.")
            return
        cmd_done(sys.argv[2])
    
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Please provide the task ID to mark done.")
            return
        cmd_delete(sys.argv[2])
    
    elif command == "clear":
        cmd_clear()
    
    elif command == "edit":
        if len(sys.argv) < 4:
            print("Please provide the task ID and the new title.\nExample:\n  python todo.py edit 3 \"Buy bread instead\"")
            return
        id = sys.argv[2]
        title = " ".join(sys.argv[3:])
        cmd_edit(id , title)
    
    elif command == "undo":
        print("true")
        cmd_undo()
    
    else:
        print("Unknown command.\n")
        print(USAGE)
        
        
if __name__ == "__main__":
    main()