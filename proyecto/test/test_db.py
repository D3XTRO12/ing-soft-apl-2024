import unittest
from flask import current_app
from app import create_app, db
from sqlalchemy import text

class DbTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_db_connection(self):
        result = db.session.query(text("'Aloha'")).one()
        self.assertEqual(result[0], "Aloha")