from flask import Flask
from flask_marshmallow import Marshmallow
from flask_restful import Api
import os
from app.config import config
from pdchaos.middleware.contrib.flask.flask_middleware import FlaskMiddleware
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

ma = Marshmallow()
middleware = FlaskMiddleware()
db = SQLAlchemy()
metadata =db.metadata

def create_app() -> None:
    app_context = os.getenv('FLASK_CONTEXT')
    app = Flask(__name__)
    api = Api(app)
    load_dotenv()
    
    db_parameters = {
        "user": os.getenv('DB_USER'),
        "password": os.getenv('DB_PASSWORD'),
        "host": os.getenv('DB_HOST'),  # Se puede cambiar si es necesario
        "port": os.getenv('DB_PORT'),  # Puerto por defecto de PostgreSQL
        "dbname": os.getenv('DB_NAME')
    }
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@db:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    
    #inicializar base de datos
    db.init_app(app)    
    migrate = Migrate(app)
    migrate.init_app(app, db)

    
    f = config.factory(app_context if app_context else 'development')
    app.config.from_object(f)

    app.config['CHAOS_MIDDLEWARE_APPLICATION_NAME'] = 'vehicle_ms'
    app.config['CHAOS_MIDDLEWARE_APPLICATION_env'] = 'development'
    middleware.init_app(app)
    ma.init_app(app)
    
    from app.resources import home, GetAllVehicles, FindVehicleById, UpdateVehicle, AddVehicle, DeleteVehicle
    app.register_blueprint(home, url_prefix='/api/v1')
    api.add_resource(GetAllVehicles, '/get-all-autos')
    api.add_resource(AddVehicle, '/add-auto')
    api.add_resource(FindVehicleById, '/auto/<int:vehicle_id>')  # Nuevo endpoint para buscar un auto por ID
    api.add_resource(DeleteVehicle, '/delete-auto/<int:vehicle_id>')
    api.add_resource(UpdateVehicle, '/update-auto/<int:vehicle_id>')
    
    @app.shell_context_processor    
    def ctx():
        return {"app": app}
    
    return app
