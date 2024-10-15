from app.models.user import User
from app.repository.repository_base import Create, Read, Update, Delete
from app import db

class UserRepository(Create, Read, Update, Delete):

    def __init__(self):
        self.__model = User

    def find_all(self):
        try:
            users = db.session.query(self.__model).all()
            return users
        except Exception as e:
            raise e("An error occurred while trying to retrieve the users")
        
    def find_by_id(self, id):
        try:
            entity = db.session.query(self.__model).filter(self.__model.id == id).one()
            return entity
        except Exception as e:
            raise e("An error occurred while trying to retrieve the user")
    
    def find_by_name(self, username):
        try:
            entity = db.session.query(self.__model).filter(self.__model.username == username).one()
            return entity
        except Exception as e:
            raise e("An error occurred while trying to retrieve the user")
        
    def create(self, entity):
        db.session.add(entity)
        db.session.commit()
        return entity
    
    def update(self, entity_id, updated_data):
        try:
            user = self.find_by_id(entity_id)

            if user:
                for key, value in updated_data.items():
                    setattr(user, key, value)

                db.session.commit()
                return user
            else:
                return None
        except Exception as e:
            db.session.rollback()
            raise Exception("An error occurred while trying to update the user")
        
    def delete(self, id):
        entity = self.find_by_id(id)
        db.session.delete(entity)
        db.session.commit()
        return entity