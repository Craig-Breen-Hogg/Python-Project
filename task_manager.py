import json
from pathlib import Path

DATA = Path("tasks.json")

def load_tasks():
    if DATA.exists():
        return json.loads(DATA.read_text())
    return []

def save_tasks(tasks):
    DATA.write_text(json.dumps(tasks, indent=2))

def add_task():
    tasks = load_tasks()
    task = input("Task name: ")
    tasks.append({"task": task, "done": False})
    save_tasks(tasks)

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return

    for i, task in enumerate(tasks, 1):
        status = "✔" if task["done"] else "✗"
        print(f"{i}. [{status}] {task['task']}")

def menu():
    while True:
        print("\n1) Add task\n2) List tasks\n3) Exit")
        choice = input("Choose: ")
        if choice == "1":
            add_task()
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            break

if __name__ == "__main__":
    menu()
