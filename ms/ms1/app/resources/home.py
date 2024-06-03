import random
from flask import jsonify, Blueprint, request

home = Blueprint('home', __name__)

@home.route('/', methods=['GET'])
def index():
    ip_add = request.remote_addr
    resp = jsonify({"microservicio ip": ip_add, "status": "ok"})
    resp.status_code = random.choice([200, 404])
    return resp

@home.route('/compensation', methods=['GET'])
def compensation():
    resp = jsonify({"microservicio": "Compensation 1", "status": "ok"})
    resp.status_code = 200
    return resp