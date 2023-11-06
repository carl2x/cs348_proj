"""Defines all the functions related to the database"""
from app import db
from sqlalchemy import text

def fetch_todo() -> list:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute(text("Select * from tasks;")).fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "id": result[0],
            "task": result[1],
            "status": result[2],
            "priority": result[3],
            "duration": result[4]
        }
        todo_list.append(item)

    return todo_list


def update_task_entry(task_id: int, data: dict) -> None:
    """Updates task description, priority, and duration based on given `task_id`

    Args:
        task_id (int): Targeted task_id
        data (dict): Updated data

    Returns:
        None
    """
    conn = db.connect()
    task, priority, duration = data["task"], data["priority"], int(data["duration"])
    query = text('UPDATE tasks SET task = :task, priority = :priority, duration = :duration WHERE id = :task_id')
    conn.execute(query, {"task": task, "priority": priority, "duration": duration, "task_id": task_id})
    conn.commit()
    conn.close()


def update_status_entry(task_id: int, status: str) -> None:
    """Updates task status based on given `task_id`

    Args:
        task_id (int): Targeted task_id
        text (str): Updated status

    Returns:
        None
    """
    conn = db.connect()
    query = text('Update tasks set status = "{}" where id = {};'.format(status, task_id))
    conn.execute(query)
    conn.commit()
    conn.close()


def insert_new_task(data: dict) -> int:
    """Insert new task to todo table.

    Args:
        text (str): Task description

    Returns: The task ID for the inserted entry
    """

    conn = db.connect()
    task, priority, duration = data["task"], data["priority"], (data["duration"])
    query = text('Insert Into tasks (task, status, priority, duration) VALUES ("{}", "{}", "{}", "{}");'
                 .format(task, "Todo", priority, duration))
    conn.execute(query)
    query_results = conn.execute(text("Select LAST_INSERT_ID();"))
    query_results = [x for x in query_results]
    task_id = query_results[0][0]
    conn.commit()
    conn.close()

    return task_id


def remove_task_by_id(task_id: int) -> None:
    """ remove entries based on task ID """
    conn = db.connect()
    query = text('Delete From tasks where id={};'.format(task_id))
    conn.execute(query)
    conn.commit()
    conn.close()