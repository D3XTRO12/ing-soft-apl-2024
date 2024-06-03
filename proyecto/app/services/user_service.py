from ..repo.user_repository import UserRepository
from app import db

class UserService:
    def __init__(self):
        self.__repo = UserRepository()

    def find_by_name(self, name):
        return self.__repo.find_by_name(name)

    def create(self, entity):
        return self.__repo.create(entity)
