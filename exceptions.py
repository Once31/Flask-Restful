from werkzeug.exceptions import HTTPException

class ToDoAlreadyExists(HTTPException):
    def __init__(self, message='Todo Item with the name already exists',code=400):
       self.message = message
       self.code = code
       print('by by')
       super().__init__()


class ToDoDoesNotExists(HTTPException):
    def __init__(self, message="Todo Item does not exists", code=400):
        self.message = message
        self.code = code
        super().__init__()