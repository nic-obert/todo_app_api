from flask import Flask, request, Response
import sqlite3
from os import path
import json


app = Flask(__name__)
DATABASE = 'database.db'
API_KEY = 'p5nsaSjf847MNdss--12'



def create_database():
    print('\nCreating new database since no database was found\n')
    with sqlite3.connect(DATABASE) as conn:
        db = conn.cursor()
        db.execute(
            'CREATE TABLE todos (\
                title VARCHAR (32) NOT NULL, \
                desc VARCHAR (1024) NOT NULL, \
                dateCreated VARCHAR (10) NOT NULL\
            );')
        conn.commit()


def check_database():
    if not path.exists(DATABASE):
        create_database()


def get_todos() -> list:
    with sqlite3.connect(DATABASE) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT rowid, title, desc, dateCreated FROM todos')
        todos = [dict(row) for row in cursor.fetchall()]

    return todos


def write_todo(todo: dict) -> str:
    """
        writes the new todo to the database and
        returns the new todo's id in the database
    """
    print(todo)
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO todos VALUES (?,?,?)',
            (todo["title"], todo["desc"], todo["dateCreated"]))
        conn.commit()
    return str(cursor.lastrowid)


def delete_todo(todo_id) -> None:
    print(todo_id)
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(f'DELETE FROM todos WHERE rowid=?', (todo_id,))
        conn.commit()


def edit_todo(todo: dict) -> None:
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE todos SET title=?, desc=? WHERE rowid=?',
            (todo['title'], todo['desc'], todo['rowid']))
        conn.commit()



@app.route('/edit', methods=['POST'])
def edit():
    try:
        if not request.form['apiKey'] == API_KEY:
            # wrong api key
            return Response('Access denied', status=403)
    except KeyError:
        # no api key provided
        return Response('Access denied', status=403)
    
    try:
        todo = {
            'title': request.form['title'],
            'desc': request.form['desc'],
            'rowid': request.form['rowid']
        }
    except KeyError:
        return Response('Invalid form', status=400)
    
    edit_todo(todo)
    return Response(response='Success', status=200)


@app.route('/delete', methods=['POST'])
def delete():
    try:
        if not request.form['apiKey'] == API_KEY:
            # wrong api key
            return Response('Access denied', status=403)
    except KeyError:
        # no api key provided
        return Response('Access denied', status=403)
    
    try:
        delete_todo(request.form['rowid'])
    except KeyError:
        return Response('Invalid form', status=400)

    return Response(response='Success', status=200)


@app.route('/fetch', methods=['POST'])
def fetch():
    
    try:
        if not request.form['apiKey'] == API_KEY:
            # wrong api key
            return Response('Access denied', status=403)
    except KeyError:
        # no api key provided
        return Response('Access denied', status=403)

    todos = json.JSONEncoder().encode(get_todos())
    print(todos)
    
    return Response(response=todos, status=200)


@app.route('/add', methods=['POST'])
def add():
    try:
        if not request.form['apiKey'] == API_KEY:
            return Response('Access denied', status=403)
    except KeyError:
        return Response('Access denied', status=403)

    try:
        todo = {
            'title': request.form['title'],
            'desc': request.form['desc'],
            'dateCreated': request.form['dateCreated']
        }
    except KeyError:
        return Response('Invalid form', status=400)

    rowid: str = write_todo(todo)
    
    return Response(response=rowid, status=200)


if __name__ == "__main__":

    check_database()
    app.run(debug=True, host='127.0.0.1', port=5000)

else:

    check_database()
