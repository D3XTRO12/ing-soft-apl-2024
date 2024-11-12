from flask import jsonify, Blueprint, request
from app.services.user_service import UserService
from app.schemas.user_schema import UserSchema
# NUEVO: Importaciones para telemetría
from opentelemetry import trace
from app import trace_user_operation  # El decorador que creamos
from opentelemetry.trace.status import Status, StatusCode

user = Blueprint('user', __name__)
user_schema = UserSchema()
# NUEVO: Obtener un tracer para este módulo
tracer = trace.get_tracer(__name__)

def get_user_service():
    return UserService()

# NUEVO: Mejorado para incluir telemetría
def handle_exception(e, message, span=None):
    """
    Maneja excepciones y las registra en telemetría si hay un span activo
    """
    if span:
        span.set_status(Status(StatusCode.ERROR))
        span.record_exception(e)
        span.set_attribute("error.message", message)
    return jsonify({"error": message, "exception": str(e)}), 500

# NUEVO: Mejorado para incluir telemetría
def get_user_response(user, success_code=200, not_found_message="User not found", span=None):
    """
    Genera respuesta y registra el resultado en telemetría
    """
    if user:
        if span:
            span.set_attribute("response.status_code", success_code)
            span.set_attribute("user.found", True)
        return jsonify({"user": user_schema.dump(user)}), success_code
    else:
        if span:
            span.set_attribute("response.status_code", 404)
            span.set_attribute("user.found", False)
        return jsonify({"error": not_found_message}), 404

@user.route('/get_all', methods=['GET'])
@trace_user_operation("get_all_users")
def find_all():
    current_span = trace.get_current_span()
    try:
        users = get_user_service().find_all()
        if current_span:
            current_span.set_attribute("users.count", len(users))
        return jsonify({"users": user_schema.dump(users, many=True)}), 200
    except Exception as e:
        return handle_exception(e, "An error occurred while trying to retrieve the users", current_span)

@user.route('/get/<int:user_id>', methods=['GET'])
@trace_user_operation("get_user_by_id")
def get_user_by_id(user_id):
    current_span = trace.get_current_span()
    try:
        if current_span:
            current_span.set_attribute("user.id", user_id)
        user = get_user_service().find_by_id(user_id)
        return get_user_response(user, span=current_span)
    except Exception as e:
        return handle_exception(e, "An error occurred while trying to retrieve the user", current_span)

@user.route('/get_by_name/<string:name>', methods=['GET'])
@trace_user_operation("get_user_by_name")
def find_by_name(username):
    current_span = trace.get_current_span()
    try:
        if current_span:
            current_span.set_attribute("user.username", username)
        user = get_user_service().find_by_name(username)
        return get_user_response(user, span=current_span)
    except Exception as e:
        return handle_exception(e, "An error occurred while trying to retrieve the user", current_span)

@user.route('/add', methods=['POST'])
@trace_user_operation("create_user")
def add_user():
    current_span = trace.get_current_span()
    try:
        if current_span:
            current_span.set_attribute("request.body_size", len(request.get_data()))
        user = user_schema.load(request.json)
        created_user = get_user_service().create(user)
        if current_span:
            current_span.set_attribute("user.created_id", created_user.id)
        return get_user_response(created_user, 201, span=current_span)
    except Exception as e:
        return handle_exception(e, "An error occurred while trying to create the user", current_span)

@user.route('/delete/<int:user_id>', methods=['DELETE'])
@trace_user_operation("delete_user")
def delete_user(user_id):
    current_span = trace.get_current_span()
    try:
        if current_span:
            current_span.set_attribute("user.id", user_id)
        user = get_user_service().find_by_id(user_id)
        if user:
            deleted_user = get_user_service().delete(user_id)
            if current_span:
                current_span.set_attribute("user.deleted", True)
            return get_user_response(deleted_user, 204, span=current_span)
        if current_span:
            current_span.set_attribute("user.deleted", False)
        return get_user_response(None, span=current_span)
    except Exception as e:
        return handle_exception(e, "An error occurred while trying to delete the user", current_span)

@user.route('/update/<int:user_id>', methods=['PUT'])
@trace_user_operation("update_user")
def update_user(user_id):
    current_span = trace.get_current_span()
    try:
        if current_span:
            current_span.set_attribute("user.id", user_id)
            current_span.set_attribute("request.body_size", len(request.get_data()))
        
        user_service = get_user_service()
        user = user_service.find_by_id(user_id)
        
        if user:
            updated_user_data = request.json
            for key, value in updated_user_data.items():
                setattr(user, key, value)
            user_service.update(user)
            if current_span:
                current_span.set_attribute("user.updated", True)
                current_span.set_attribute("user.fields_updated", len(updated_user_data))
            return get_user_response(user, span=current_span)
        
        if current_span:
            current_span.set_attribute("user.updated", False)
        return get_user_response(None, span=current_span)
    except Exception as e:
        return handle_exception(e, "An error occurred while trying to update the user", current_span)