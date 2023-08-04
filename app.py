from flask import Flask
from flask_restful import Resource, Api, abort
from exceptions import ToDoAlreadyExists, ToDoDoesNotExists
import sqlite3
import json
from flask import request
from flask import jsonify

from flask_cors import CORS

app = Flask(__name__)

CORS(app)

class CustomApi(Api):
    def handle_error(self, e):
        return {'code': e.code, 'message': e.message}, 400
    
api = CustomApi(app)    


def get_db_connection():
    conn = sqlite3.connect('todo.db')
    conn.row_factory = sqlite3.Row #to make each row return dict instead of tuple
    return conn

def get_todos(conn):
   results = conn.execute('SELECT * FROM todos').fetchall()
   results = [dict(row) for row in results]
   return results
   

def createToDo(conn, todo):
    conn.execute('INSERT INTO todos (name, status) values(?,?)',(todo['name'], todo['status']))
    conn.commit()
    return get_todos(conn)

def updateToDo(conn, todo):
    conn.execute('UPDATE todos set name = ? , status = ? where id = ?', ( todo['name'], todo['status'], todo['id']))
    conn.commit()
    return get_todos(conn)

def deleteTodo(conn, id):
    conn.execute('DELETE FROM todos WHERE id = ?', (id))
    conn.commit()
    return get_todos(conn)

class ToDo(Resource):
    def get(self):
        conn = get_db_connection()
        todos = get_todos(conn)
        conn.close()
        return todos

    def post(self):
        conn = get_db_connection()
        todos = get_todos(conn)
        todo = request.json
        for td in todos:
            if td['name'] == todo['name']:
                raise ToDoAlreadyExists(f"Todo [{todo['name']}] already exits", 400)
        todos = createToDo(conn, todo)
        conn.close()
        return todos, 201
    
    def put(self):
        conn = get_db_connection()
        todos = get_todos(conn)
        todo = request.json
        print('todo',todo)
        ids = [todo['id'] for todo in todos]
        print(ids)
        if todo['id'] not in ids:
            raise ToDoDoesNotExists(f"Todo with ID [{todo['id']}] doesn't exits", 400)

        todos = updateToDo(conn, todo)
        conn.close()
        return todos

    def delete(self):
        conn = get_db_connection()
        id = request.args['id']
        todos = get_todos(conn)
        ids = [str(todo['id']) for todo in todos] 
        if id not in ids :
            raise ToDoDoesNotExists(f"Todo with ID [{id}] doesn't exits", 400)           
        todos = deleteTodo(conn, id)
        return todos

class HelloWorld(Resource):
    def get(self):
        # raise ToDOAlreadyExists("Todo Exists", 400)
        return {"message": 'hello world'}

api.add_resource(ToDo, '/api/todos')
api.add_resource(HelloWorld, '/hello') 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)