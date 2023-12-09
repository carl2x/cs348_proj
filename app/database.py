"""Defines all the functions related to the database"""
from app import db
from sqlalchemy import text


def fetch_todo() -> list:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute(text("SELECT * FROM tasks ORDER BY id DESC;")).fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "id": result[0],
            "task": result[1],
            "status": result[2],
            "priority": result[3],
            "duration": result[4],
        }
        todo_list.append(item)

    return todo_list


def fetch_report() -> dict:
    """Fetches the latest report from the reports table

    Returns:
        A dictionary representing the latest report
    """

    conn = db.connect()
    query_results = conn.execute(
        text("SELECT * FROM reports ORDER BY id DESC LIMIT 1;")
    ).fetchone()
    conn.close()
    assert query_results is not None
    report = {
        "id": query_results[0],
        "total_todos": query_results[1],
        "total_completed": query_results[2],
        "total_in_progress": query_results[3],
        "completion_rate": query_results[4],
        "avg_duration": query_results[5],
        "priority": query_results[6]
    }

    return report


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
    query = text(
        "UPDATE tasks SET task = :task, priority = :priority, duration = :duration WHERE id = :task_id"
    )
    conn.execute(
        query,
        {"task": task, "priority": priority, "duration": duration, "task_id": task_id},
    )
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
    query = text(
        'Update tasks set status = "{}" where id = {};'.format(status, task_id)
    )
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
    query = text(
        'Insert Into tasks (task, status, priority, duration) VALUES ("{}", "{}", "{}", "{}");'.format(
            task, "Todo", priority, duration
        )
    )
    conn.execute(query)
    query_results = conn.execute(text("Select LAST_INSERT_ID();"))
    query_results = [x for x in query_results]
    task_id = query_results[0][0]
    conn.commit()
    conn.close()

    return task_id


def remove_task_by_id(task_id: int) -> None:
    """remove entries based on task ID"""
    conn = db.connect()
    query = text("Delete From tasks where id={};".format(task_id))
    conn.execute(query)
    conn.commit()
    conn.close()


def generate_report(data: dict) -> int:
    """Insert new report to reports table.

    Args:
        data (dict): Report data

    Returns: The report ID for the inserted entry
    """

    conn = db.connect()
    priority = data["priority"]
    priority_filter = "" if priority == "All" else f'AND priority = "{priority}"'

    # Total number of TODOs
    query = text(f"SELECT COUNT(*) FROM tasks WHERE 1 {priority_filter}")
    total_todos = conn.execute(query).scalar()
    assert total_todos is not None

    # Total number of TODOs with the completed status
    query = text(
        f"SELECT COUNT(*) FROM tasks WHERE status = 'complete' {priority_filter}"
    )
    total_completed = conn.execute(query).scalar()
    assert total_completed is not None

    # Total number of TODOs with the in progress status
    query = text(
        f"SELECT COUNT(*) FROM tasks WHERE status = 'in progress' {priority_filter}"
    )
    total_in_progress = conn.execute(query).scalar()

    # Completion rate: num completed / total number of todos
    completion_rate = total_completed / total_todos if total_todos > 0 else 0

    # Average duration of TODOs
    query = text(f"SELECT AVG(duration) FROM tasks WHERE 1 {priority_filter}")
    avg_duration = conn.execute(query).scalar()

    query = text(
        "INSERT INTO reports (id, total_todos, total_completed, total_in_progress, completion_rate, avg_duration, priority) VALUES (1, :total_todos, :total_completed, :total_in_progress, :completion_rate, :avg_duration, :priority) ON DUPLICATE KEY UPDATE total_todos = VALUES(total_todos), total_completed = VALUES(total_completed), total_in_progress = VALUES(total_in_progress), completion_rate = VALUES(completion_rate), avg_duration = VALUES(avg_duration), priority = VALUES(priority)"
    )
    conn.execute(
        query,
        {
            "total_todos": total_todos,
            "total_completed": total_completed,
            "total_in_progress": total_in_progress,
            "completion_rate": completion_rate,
            "avg_duration": avg_duration,
            "priority": priority,
        },
    )
    conn.commit()
    conn.close()

    return 1
