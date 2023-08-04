import unittest
import app

unittest.TestLoader.sortTestMethodsUsing = None
BASE_URL = '/api/todos'

class ToDoTest(unittest.TestCase):
    def setUp(self) -> None:
        self.app = app.app
        self.app.testing = True
        self.client = self.app.test_client()

    def test_get_todos(self):
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, 200)

    def test_post_todos_success(self):
        response = self.client.post(BASE_URL, json={"id": 3, "name": "hello once", "status": "pending"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.json), 3)

    def test_post_todos_error(self):
        response = self.client.post(BASE_URL, json={"id": 2, "name": "new once", "status": "complete"})
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()