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
        cursor.execute('SELECT * FROM todos')
        todos = [dict(row) for row in cursor.fetchall()]
    return todos


def write_todo(todo: dict) -> None:
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f'INSERT INTO todos VALUES (\
                "{todo["title"]}", \
                "{todo["desc"]}", \
                "{todo["dateCreated"]}"\
            )')
        conn.commit()


def delete_todo(todo_id) -> None:
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(f'DELETE FROM todos WHERE rowid={todo_id}')
        conn.commit()



@app.route('/delete', methods=['POST'])
def delete():
    if not request.form['apiKey'] == API_KEY:
        return Response('Access denied', status=403)
    
    delete_todo(request.form['id'])
    return Response(response='Success', status=200)


@app.route('/fetch', methods=['POST'])
def fetch():
    if not request.form['apiKey'] == API_KEY:
        return Response('Access denied', status=403)

    todos = json.JSONEncoder().encode(get_todos())
    print(todos)
    
    return Response(response=todos, status=200)


@app.route('/add', methods=['POST'])
def add():
    if not request.form['apiKey'] == API_KEY:
        return Response('Access denied', status=403)

    todo = {
        'title': request.form['title'],
        'desc': request.form['desc'],
        'dateCreated': request.form['dateCreated']
    }

    write_todo(todo)
    
    return Response(response='Success', status=200)

if __name__ == "__main__":

    check_database()
    app.run(debug=True, host='192.168.1.8', port=5000)

else:

    check_database()
