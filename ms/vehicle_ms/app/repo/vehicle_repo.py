from ..models.vehicle.vehicle_model import Vehicle
from .repo_base import Read, Create, Delete
from app import db

class VehicleRepository(Read, Create, Delete):

    def __init__(self):
        self.__model = Vehicle
    
    # Read Section
    def find_all(self):
        try:
            categories = db.session.query(self.__model).all()
            return categories
        except Exception as e:
            raise Exception("Error al obtener la lista de categorias: " + str(e))
        
    def find_by_id(self, id):
        try:
            entity = db.session.query(self.__model).filter(self.__model.id == id).one()
            return entity
        except Exception as e:
            raise Exception("Error al obtener usuario por ID: " + str(e))
        
        
    def find_by_time(self, time):
        return db.session.query(self.__model).filter(self.__model.__time == time).one()

    # Create Section
    def create(self, entity):
        db.session.add(entity)
        db.session.commit()
        return entity
    
    # Delete Section
    def delete(self, id):
        entity = self.find_by_id(id)
        if entity:
            db.session.delete(entity)
            db.session.commit()
            return entity
        else:
            raise Exception("Error al eliminar usuario: El usuario con ID {} no existe".format(id))
    