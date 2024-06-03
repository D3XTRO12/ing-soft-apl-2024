import random
from flask import jsonify, Blueprint

home = Blueprint('home', __name__)

@home.route('/', methods=['GET'])
def index():
    resp = jsonify({"microservicio": "3", "status": "ok"})
    resp.status_code = random.choice([200, 404])
    return resp

@home.route('/compensation', methods=['GET'])
def compensation():
    resp = jsonify({"microservicio": "Compensation 3", "status": "ok"})
    resp.status_code = 200
    return resp