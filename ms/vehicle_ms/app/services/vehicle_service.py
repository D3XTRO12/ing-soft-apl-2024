from app import db
from ..repo.vehicle_repo import VehicleRepository as VehicleRepo
from ..models.vehicle.vehicle_model import Vehicle

class VehicleService:
    
    def __init__(self):
        self.__repo = VehicleRepo()
        
    
    def create(self, entity):
        return self.__repo.create(entity)
    
    def find_all(self):
        try:
            vehicle = self.__repo.find_all()
            if vehicle:
                return vehicle
            else:
                return []
        except Exception as e:
            raise Exception("Error al obtener vehiculos: " + str(e))
    
    def find_by_id(self, entity_id):
        try:
            entity = self.__repo.find_by_id(entity_id)
            if entity:
                return entity
            else:
                return []
        except Exception as e:
            raise Exception("Error al obtener vehiculo por id: " + str(e))
    
    def find_by_time(self, entity_time):
        try:
            entity = self.__repo.find_by_time(entity_time)
            if entity:
                return entity
            else:
                return []
        except Exception as e:
            raise Exception("Error al obtener vehiculo por tiempo: " + str(e))
    
    def update(self, entity = Vehicle) -> Vehicle:
        vehicle = self.__repo.find_by_id(entity.id)
        if vehicle:
            vehicle.time = entity.time
            vehicle.tyre_type = entity.tyre_type
            vehicle.fuel = entity.fuel
            vehicle.bodywork = entity.bodywork
            db.session.commit()
        return vehicle
    
    def delete(self, entity_id):
        return self.__repo.delete(entity_id)