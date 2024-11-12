import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    # Configuración de base de datos
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Usa SQLite temporalmente para prueba

    # Inicializa la base de datos
    db.init_app(app)

    # Registro de blueprint
    from app.controllers.health_controller import health
    app.register_blueprint(health, url_prefix='/api')

    # Configuración de logs
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.debug("Aplicación iniciada")

    return app
