def fetch_todo() -> list:
    todo_list = [
        {
            "id": 1,
            "task": "Do the dishes",
            "status": "Not Started"
        },
        {
            "id": 2,
            "task": "Do the laundry",
            "status": "Not Started"
        },
        {
            "id": 3,
            "task": "Do the chores",
            "status": "Not Started"
        }
    ]
    return todo_list

def insert_new_task(task: str) -> None:
    pass

def update_task_entry(task_id: int, task: str) -> None:
    pass

def update_status_entry(task_id: int, status: str) -> None:
    pass

def remove_task_by_id(task_id: int) -> None:
    pass
