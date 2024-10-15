from flask_restful import Resource, reqparse
from app.services.vehicle_service import VehicleService
from app.mapping import VehicleSchema


class UpdateVehicle(Resource):
    def put(self, vehicle_id):
        vehicle_service = VehicleService()
        try:
            vehicle = vehicle_service.find_by_id(vehicle_id)
            if vehicle:
                updated_vehicle_data = VehicleSchema().load(reqparse.request.json, partial=True)
                for key, value in updated_vehicle_data.items():
                    setattr(vehicle, key, value)
                vehicle_service.update(vehicle)
                return {"vehicle": VehicleSchema().dump(vehicle)}, 200
            else:
                return {"error": "Vehiculo no encontrado"}, 404
        except Exception as e:
            return {"error": f"Error al actualizar Vehiculo: {str(e)}"}, 500

