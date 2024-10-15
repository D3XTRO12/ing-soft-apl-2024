import os
from flask import Flask
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
metadata = db.metadata

def create_app():

    app = Flask(__name__)
    load_dotenv()

    # Load the configuration
    db_parameters = {
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "database": os.getenv("DB_NAME")
    }
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{db_parameters['user']}:{db_parameters['password']}@{db_parameters['host']}:{db_parameters['port']}/{db_parameters['database']}"

    # Initialize the database
    db.init_app(app)


    migrate = Migrate(app)
    migrate.init_app(app, db)

    from app.controllers.user_controllers import user
    app.register_blueprint(user, url_prefix='/user')
    #app.register_blueprint(home, url_prefix='')
    #app.register_blueprint(category, url_prefix='/category')
    #app.register_blueprint(vehicle, url_prefix='/vehicle')

    @app.shell_context_processor
    def ctx():
        return {"app":app}
    
    return app