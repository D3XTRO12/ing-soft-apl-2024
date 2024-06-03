import random
from flask import jsonify, Blueprint
from app.services import AtomicProcess

home = Blueprint('home', __name__)

@home.route('/', methods=['GET'])
def index():
    resp = jsonify({"microservicio": "3", "status": "ok"})
    resp.status_code = random.choice([200, 404])
    return resp

@home.route('/atomic-process', methods=['GET'])
def atomic_process():
    process = AtomicProcess()
    result = process.execute()
    resp = result.json()
    
    return resp, result.status_code