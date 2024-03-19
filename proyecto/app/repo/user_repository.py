from app.models.user.user_model import User
from .repository_base import Read, Create
from app import db


class UserRepository(Create, Read):
        
    def __init__(self):
        self.__model = User

    #Read Section    
    def find_by_name(self, name):
        try:
            entity = db.session.query(self.__model).filter(self.__model.username == name).one()
            return entity
        except Exception as e:
            raise Exception("Error al obtener usuario por nombre de usuario: " + str(e))
    
    #Create Section
    def create(self, entity):
        db.session.add(entity)
        db.session.commit()
        return entity
        
