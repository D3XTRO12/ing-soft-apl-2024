import random
from flask import jsonify, Blueprint, request

home = Blueprint('home', __name__)

@home.route('/', methods=['GET'])
def index():
    ip_addr = request.remote_addr
    resp = jsonify({"microservicio": "2", "ip address": ip_addr, "status": "ok"})
    resp.status_code = random.choice([200, 200])
    return resp

@home.route('/compensation', methods=['GET'])
def compensation():
    resp = jsonify({"microservicio": "Compensation 2", "status": "ok"})
    resp.status_code = 200
    return resp