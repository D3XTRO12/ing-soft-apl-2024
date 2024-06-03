import os
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
metadata = db.metadata
mail = Mail()
def create_app():
    load_dotenv()
    config_name = os.getenv("FLASK_ENV")
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("postgres_DEV_DATABASE_URI")
    db.init_app(app)
    mail.init_app(app)
    with app.app_context():
        db.create_all()
    
    from app.controllers import mail_bp
    app.register_blueprint(mail_bp)
    
    app.config['DEBUG'] = True
    
    @app.shell_context_processor
    def ctx():
        return {"app": app}
    return app
