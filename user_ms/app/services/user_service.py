from app.repository.user_repository import UserRepository

#from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class UserService:
    def __init__(self):
        self.__repository = UserRepository()

    def find_all(self):
        try:
            users = self.__repository.find_all()
            if users:
                return users
            else:
                return []
        except Exception as e:
            raise e("An error occurred while trying to retrieve the users")
        
    def find_by_id(self, entity_id):
        try:
            entity = self.__repository.find_by_id(entity_id)
            if entity:
                return entity
            else:
                return None
        except Exception as e:
            raise e("An error occurred while trying to retrieve the user")
        
    def find_by_name(self, name):
        try:
            entity = self.__repository.find_by_name(name)
            if entity:
                return entity
            else:
                return None
        except Exception as e:
            raise e("An error occurred while trying to retrieve the user")
    
    def create(self, entity):
        return self.__repository.create(entity)
    
    def delete(self, entity_id):
        return self.__repository.delete(entity_id)
    
    def update(self, entity):
        try:
            user = self.__repository.find_by_id(entity.id)

            if user:
                user.name = entity.name
                user.dni = entity.dni
                user.email = entity.email
                user.gender = entity.gender
                user.address = entity.address
                user.phone = entity.phone

                db.session.commit()
                return user
            else:
                return None
        except Exception as e:
            db.session.rollback()
            raise Exception("An error occurred while trying to update the user")