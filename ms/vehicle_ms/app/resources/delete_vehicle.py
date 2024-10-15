from flask_restful import Resource
from app.services.vehicle_service import VehicleService
from app.mapping import VehicleSchema

class DeleteVehicle(Resource):
    def delete(self, vehicle_id):
        vehicle_service = VehicleService()
        try:
            vehicle = vehicle_service.find_by_id(vehicle_id)
            if vehicle:
                vehicle_service.delete(vehicle_id)
                return {"message": "Vehiculo eliminado"}, 200
            else:
                return {"error": "Vehiculo no encontrado"}, 404
        except Exception as e:
            return {"error": f"Error al eliminar el vehiculo: {str(e)}"}, 500