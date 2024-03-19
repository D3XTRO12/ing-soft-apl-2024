import os 
from flask import Flask
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
metadata = db.metadata

def create_app():
    config_name = os.getenv("FLASK_ENV")
    
    app = Flask(__name__)
    load_dotenv()
    db_url = '/home/d3xtro/Documents/FACULTAD/4 to/INGENIERIA DE SOFT/proyecto/ing.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_url
    db.init_app(app)

    @app.shell_context_processor
    def ctx():
        return {"app": app}
    return app