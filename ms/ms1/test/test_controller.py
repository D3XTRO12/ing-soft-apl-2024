import unittest
from flask import current_app
from app import create_app

class ControllerTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_app(self):
        self.assertIsNotNone(current_app)
    
    def test_index(self):
        client = self.app.test_client(use_cookies=True)
        response = client.get('http://localhost:5001/api/v1/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'microservicio', response.data)
        self.assertIn(b'status', response.data)

if __name__ == '__main__':
    unittest.main()