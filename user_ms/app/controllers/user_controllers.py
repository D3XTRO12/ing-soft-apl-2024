from flask import jsonify, Blueprint, request
from app.services.user_service import UserService
from app.schemas.user_schema import UserSchema

user = Blueprint('user', __name__)
user_schema = UserSchema()

def get_user_service():
    return UserService()

def handle_exception(e, message):
    return jsonify({"error": message, "exception": str(e)}), 500

def get_user_response(user, success_code=200, not_found_message="User not found"):
    if user:
        return jsonify({"user": user_schema.dump(user)}), success_code
    else:
        return jsonify({"error": not_found_message}), 404
    
@user.route('/', methods=['GET'])
def home():
    return jsonify({"message": "User microservice"}), 200

@user.route('/get_all', methods=['GET'])
def find_all():
    try:
        users = get_user_service().find_all()
        return jsonify({"user": user_schema.dump(users, many=True)}), 200
    except Exception as e:
        return handle_exception(e, "An error occurred while trying to retrieve the users")
    
@user.route('/get/<int:user_id>', methods=['GET'])
def get_user_by_is(user_id):
    try:
        user = get_user_service().find_by_id(user_id)
        return get_user_response(user)
    except Exception as e:
        return handle_exception(e, "An error occurred while trying to retrieve the user")

@user.route('/get_by_name/<string:name>', methods=['GET'])
def find_by_name(username):
    try:
        user = get_user_service().find_by_name(username)
        return get_user_response(user)
    except Exception as e:
        return handle_exception(e, "An error occurred while trying to retrieve the user")
    
@user.route('/add', methods=['POST'])
def add_user():
    try:
        user = user_schema.load(request.json)
        return get_user_response(get_user_service().create(user), 201)
    except Exception as e:
        return handle_exception(e, "An error occurred while trying to create the user")

@user.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = get_user_service().find_by_id(user_id)
        return get_user_response(get_user_service().delete(user_id), 204)
    except Exception as e:
        return handle_exception(e, "An error occurred while trying to delete the user")

@user.route('/update/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user_service = get_user_service()
        user = user_service.find_by_id(user_id)
        if user:
            updated_user_data = request.json
            for key, value in updated_user_data.items():
                setattr(user, key, value)
            user_service.update(user)
            return get_user_response(user)
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return handle_exception(e, "An error occurred while trying to update the user")