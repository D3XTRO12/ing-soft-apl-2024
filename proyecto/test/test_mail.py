import unittest
from app import create_app

class TestFlaskMail(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_send_email(self):
        with self.app.test_client() as client:
            response = client.get('/send-email')
            # Imprimir el contenido de la respuesta
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Email sent successfully', response.data)

if __name__ == '__main__':
    unittest.main()
