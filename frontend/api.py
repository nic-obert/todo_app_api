import json
from flask import request, Response, Flask

from backend.database import edit_todo, add_todo, delete_todo, fetch_todos
from .api_settings import API_KEY, ADD, FETCH, DELETE, EDIT


app = Flask(__name__)


@app.route(EDIT, methods=['POST'])
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


@app.route(DELETE, methods=['POST'])
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


@app.route(FETCH, methods=['POST'])
def fetch():
    
    try:
        if not request.form['apiKey'] == API_KEY:
            # wrong api key
            return Response('Access denied', status=403)
    except KeyError:
        # no api key provided
        return Response('Access denied', status=403)

    todos = json.JSONEncoder().encode(fetch_todos())
    print(todos)
    
    return Response(response=todos, status=200)


@app.route(ADD, methods=['POST'])
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

    rowid: str = add_todo(todo)
    
    return Response(response=rowid, status=200)
