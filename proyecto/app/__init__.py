import os
from flask import Flask
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
metadata = db.metadata

def create_app():
    load_dotenv()
    config_name = os.getenv("FLASK_ENV")
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DEV_DATABASE_URI")
    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.shell_context_processor
    def ctx():
        return {"app": app}
    return app
