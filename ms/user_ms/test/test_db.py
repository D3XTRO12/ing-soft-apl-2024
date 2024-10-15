import unittest
from flask import current_app
from app import create_app, db
from app.models.user import User


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_database_creation(self):
        with self.app_context:
            user = User(username='test_user', email='test@example.com', dni='12345678', gender='M', age=20, address='test address', phone='123456789', role='admin')
            db.session.add(user)
            db.session.commit()

            retrieved_user = User.query.filter_by(username='test_user').first()

            self.assertIsNotNone(retrieved_user)
            self.assertEqual(retrieved_user.email, 'test@example.com')

    def test_user_deletion(self):
        with self.app_context:
            user = User(username='test_user', email='test@example.com', dni='12345678',gender='M', age=20, address='test address', phone='123456789', role='admin')
            db.session.add(user)
            db.session.commit()

            retrieved_user = User.query.filter_by(username='test_user').first()
            self.assertIsNotNone(retrieved_user)

if __name__ == '__main__':
    unittest.main()