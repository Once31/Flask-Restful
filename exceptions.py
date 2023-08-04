from werkzeug.exceptions import HTTPException

class ToDOAlreadyExists(HTTPException):
    def __init__(self, message='Todo Item with the name already exists',code=400):
       self.message = message
       self.code = code
       print('by by')
       super().__init__()