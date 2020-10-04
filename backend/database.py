import sqlite3
from os import path

from .db_settings import DATABASE, DB_INIT, DB_FETCH, DB_EDIT, DB_ADD, DB_DELETE


def _create_database():
    print('\nCreating new database since no database was found\n')
    with sqlite3.connect(DATABASE) as conn:
        db = conn.cursor()
        db.execute(DB_INIT)
        conn.commit()


def check_database():
    if not path.exists(DATABASE):
        _create_database()



def fetch_todos() -> list:
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(DB_FETCH)
        todos = [dict(row) for row in cursor.fetchall()]

    return todos


def add_todo(todo: dict) -> str:
    """
        writes the new todo to the database and
        returns the new todo's id in the database
    """
    print(todo)
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            DB_ADD,
            (todo["title"], todo["desc"], todo["dateCreated"]))
        conn.commit()
    return str(cursor.lastrowid)


def delete_todo(todo_id) -> None:
    print(todo_id)
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            DB_DELETE,
            (todo_id,))
        conn.commit()


def edit_todo(todo: dict) -> None:
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            DB_EDIT,
            (todo['title'], todo['desc'], todo['rowid']))
        conn.commit()