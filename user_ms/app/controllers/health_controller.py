from flask import Blueprint, jsonify

health = Blueprint('health', __name__)

@health.route('/health', methods=['GET'])
def health_check():
    # Responde con un estado de "healthy"
    return jsonify({"status": "healthy"}), 200
