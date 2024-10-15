from app.models.category.category_model import Category
from app import db
from app.repository.category_repository import CategoryRepository

class CategoryService:
    def __init__(self):
        self.__repo = CategoryRepository()

    def create(self,entity):
        return self.__repo.create(entity)

    def find_all(self):
        try:
            categories = self.__repo.find_all()
            if categories:
                return categories
            else:
                return []
        except Exception as e:
            raise Exception("Error al obtener la lista de categorias: " + str(e))
    
    def find_by_id(self, entity_id):
        try:
            entity = self.__repo.find_by_id(entity_id)
            if entity:
                return entity
            else:
                return None  # Devuelve None si el usuario no se encuentra
        except Exception as e:
            raise Exception("Error al obtener usuario por ID: " + str(e))
        
    def find_by_time(self, entity_time):  #read
        try:
            entity = self.__repo.find_by_time(entity_time)
            if entity:
                return entity
            else:
                return None
        except Exception as e:
            raise Exception("Tiempo no encontrado"+str(e))
    

    def delete(self, entity_id):
        return self.__repo.delete(entity_id)
    