from flask import Flask
from flask_restful import Resource
from app.services.vehicle_service import VehicleService
from app.mapping.vehicle_schema import VehicleSchema

class GetAllVehicles(Resource):
    def get(self):
        vehicle_service = VehicleService()
        try:
            vehicles = vehicle_service.find_all()
            serialized_vehicles = VehicleSchema().dump(vehicles, many=True)
            return {"vehicles": serialized_vehicles}, 200
        except Exception as e:
            return {"error": f"Error al Obtener Vehiculos: {str(e)}"}, 500