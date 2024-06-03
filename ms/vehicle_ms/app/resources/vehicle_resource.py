from flask import Blueprint, jsonify, request
from app.services.vehicle_service import VehicleService
from app.mapping import VehicleSchema

# Crear el blueprint
vehicle = Blueprint('vehicle', __name__)
vehicle_schema = VehicleSchema()

def get_vehicle_service():
    return VehicleService()

def handle_exception(e, message):
    return jsonify({"error": f"{message}: {str(e)}"}), 500

@vehicle.route('/get-all', methods=['GET'])
def find_all():
    try:
        vehicles = get_vehicle_service().find_all()
        serialized_vehicles = vehicle_schema.dump(vehicles, many=True)
        return jsonify({"vehicles": serialized_vehicles}), 200
    except Exception as e:
        return handle_exception(e, "Error al Obtener Vehiculos")

@vehicle.route('/add', methods=['POST'])
def post_vehicle():
    try:
        vehicle_data = vehicle_schema.load(request.json)
        return jsonify({"vehicle": vehicle_schema.dump(get_vehicle_service().create(vehicle_data))}), 200
    except Exception as e:
        return handle_exception(e, "Error al agregar Vehiculo")

@vehicle.route('/delete/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    try:
        vehicle = get_vehicle_service().find_by_id(vehicle_id)
        if vehicle:
            get_vehicle_service().delete(vehicle_id)
            return jsonify({"message": "Vehiculo eliminado"}), 200
        else:
            return jsonify({"error": "Vehiculo no encontrado"}), 404
    except Exception as e:
        return handle_exception(e, "Error al eliminar el vehiculo")

@vehicle.route('/update/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    try:
        vehicle = get_vehicle_service().find_by_id(vehicle_id)
        if vehicle:
            updated_vehicle_data = vehicle_schema.load(request.json, partial=True)
            for key, value in updated_vehicle_data.items():
                setattr(vehicle, key, value)
            get_vehicle_service().update(vehicle)
            return jsonify({"vehicle": vehicle_schema.dump(vehicle)}), 200
        else:
            return jsonify({"error": "Vehiculo no encontrado"}), 404
    except Exception as e:
        return handle_exception(e, "Error al actualizar Vehiculo")

@vehicle.route('/get-all/compensation', methods=['GET'])
def compensation():
    return jsonify({"microservicio": "Compensation 2", "status": "ok"}), 200
