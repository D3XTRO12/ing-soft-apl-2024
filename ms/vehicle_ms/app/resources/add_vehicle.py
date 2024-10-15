from flask import Flask
from flask_restful import Resource, reqparse
from app.services.vehicle_service import VehicleService
from app.mapping.vehicle_schema import VehicleSchema
class AddVehicle(Resource):
    def post(self):
        vehicle_service = VehicleService()
        try:
            vehicle_data = VehicleSchema().load(reqparse.request.json)
            vehicle = vehicle_service.create(vehicle_data)
            return {"vehicle": VehicleSchema().dump(vehicle)}, 201
        except Exception as e:
            return {"error": f"Error al agregar Vehiculo: {str(e)}"}, 400