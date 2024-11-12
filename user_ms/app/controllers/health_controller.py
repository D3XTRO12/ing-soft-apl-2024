from flask import Blueprint
from opentelemetry.sdk.health.probe import HealthProbe

health = Blueprint('health', __name__)

@health.route('/health', methods=['GET'])
def health_check():
    health_probe = HealthProbe()
    return health_probe.check_status()