from flask import Flask
from flask_marshmallow import Marshmallow
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
    load_dotenv()
    
    db_parameters = {
        "user": os.getenv('DB_USER'),
        "password": os.getenv('DB_PASSWORD'),
        "host": os.getenv('DB_HOST', 'localhost'),  # Se puede cambiar si es necesario
        "port": os.getenv('DB_PORT', '5432'),  # Puerto por defecto de PostgreSQL
        "dbname": os.getenv('DB_NAME')
    }
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_parameters['user']}:{db_parameters['password']}@{db_parameters['host']}:{db_parameters['port']}/{db_parameters['dbname']}"
    
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
    
    from app.resources import home, vehicle
    app.register_blueprint(home, url_prefix='/api/v1')
    app.register_blueprint(vehicle, url_prefix='/vehicle')
    @app.shell_context_processor    
    def ctx():
        return {"app": app}
    
    return app
