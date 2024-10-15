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

    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")


    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Construcción de la cadena de conexión utilizando las variables de entorno
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    # Initialize the database
    db.init_app(app)


    migrate = Migrate(app)
    migrate.init_app(app, db)

    from .controllers import home, user_controllers
    app.register_blueprint(home, url_prefix='/api/v1')
    app.register_blueprint(user_controllers.user, url_prefix='/user')

    @app.shell_context_processor
    def ctx():
        return {"app":app}
    
    return app