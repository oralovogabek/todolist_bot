import sqlite3


DATABASE_NAME = "todo.db"


def create_database():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            task TEXT NOT NULL,
            status TEXT DEFAULT 'F'
        )
    """)

    connection.commit()
    connection.close()


def add_task(user_id: int, task: str):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO tasks (user_id, task, status) VALUES (?, ?, 'F')",
        (user_id, task)
    )

    connection.commit()
    connection.close()


def get_tasks(user_id: int):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, task, status
        FROM tasks
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (user_id,)
    )

    tasks = cursor.fetchall()

    connection.close()

    return tasks


def get_completed_tasks(user_id: int):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, task, status
        FROM tasks
        WHERE user_id = ? AND status = 'T'
        ORDER BY id DESC
        """,
        (user_id,)
    )

    tasks = cursor.fetchall()

    connection.close()

    return tasks


def delete_task(task_id: int, user_id: int):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM tasks
        WHERE id = ? AND user_id = ?
        """,
        (task_id, user_id)
    )

    connection.commit()
    connection.close()


def complete_task(task_id: int, user_id: int):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET status = 'T'
        WHERE id = ? AND user_id = ?
        """,
        (task_id, user_id)
    )

    connection.commit()
    connection.close()