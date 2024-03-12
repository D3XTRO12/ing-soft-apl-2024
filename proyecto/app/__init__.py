import os 
from flask import Flask

def create_app():
    app = Flask(__name__)


    @app.shell_context_processor
    def ctx():
        return {"app": app}
    return app