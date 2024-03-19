import unittest
from flask import current_app
from app import create_app, db
from app.models.user.user_builder import UserBuilder
from app.services.user_service import UserService

class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
    def tearDown(self):
        self.app_context.pop()
        
    def test_user(self):
        user =  UserBuilder
        user.username = "admin"
        self.assertEqual(user.username, "admin")
    def test_user_dupled(self):
        user1 = UserBuilder
        user1.username = "admin"
        user2 = UserBuilder
        user2.username = "admin"
        self.assertEqual(user1, user2)
    def test_create_user(self):
        user_builder = UserBuilder("admin")
        user = user_builder.build() 
        user_service = UserService()
        user_service.create(user)
        self.assertEqual(user_service.find_by_name("admin"), user)
        