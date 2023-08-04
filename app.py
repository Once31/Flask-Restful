from flask import Flask
from flask_restful import Resource, Api, abort
from exceptions import ToDOAlreadyExists

from flask import request

from flask_cors import CORS

app = Flask(__name__)

CORS(app)
# api = Api(app)

todoData = [
    {"id": 1, "name": "first todo", "status": "STARTED"},
    {"id": 2, "name": "learning flask...", "status": "NEW"},
]


class CustomApi(Api):
    def handle_error(self, e):
        return {'code': e.code, 'message': e.message}, 400
    
api = CustomApi(app)    

class ToDo(Resource):
    def get(self):
        return todoData

    def post(self):
        todo = request.json

        for td in todoData:
            if td['id'] == todo['id']:
                raise ToDOAlreadyExists(f"ToDo [{todo['name']}] already exists", 400)
        todoData.append(todo)
        return todoData, 201
    
    def put(self):
        todo = request.json

        for idx, td in enumerate(todoData):
            if str(td['id']) == str(todo['id']):
                todoData[idx] = todo
        
        return todoData

    def delete(self):
        for idx, td in enumerate(todoData):
            if str(td['id']) == str(request.args['id']):
                todoData.pop(idx)
                return {'message': 'Deleted', 'id': td['id']}
        return {'message': f'todo not found with id {request.args["id"]}'}


class HelloWorld(Resource):
    def get(self):
        # raise ToDOAlreadyExists("Todo Exists", 400)
        return {"message": 'hello world'}

api.add_resource(ToDo, '/api/todos')
api.add_resource(HelloWorld, '/hello') 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)