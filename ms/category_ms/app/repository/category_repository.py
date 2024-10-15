from app.models.category.category_model import Category
from app.repository.repository_base import Read, Create, Delete
from app import db

class CategoryRepository(Read, Create, Delete):
    def __init__(self):
        self.__model = Category
    
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
            raise Exception("Error al obtener categoria por ID: " + str(e))
        

    def find_by_time(self, time):
        return db.session.query(self.__model).filter(self.__model.time_category == time).one()

    # Create Section
    def create(self, entity):
        db.session.add(entity)
        db.session.commit()
        return entity
    
    # Delete Section
    def delete(self, id):
        entity = self.find_by_id(id)
        db.session.delete(entity)
        db.session.commit()
        return entity
    