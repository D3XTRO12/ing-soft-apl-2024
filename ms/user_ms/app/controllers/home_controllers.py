from flask import jsonify, Blueprint

home = Blueprint('home', __name__)

@home.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Welcome to the User Service!"}), 200