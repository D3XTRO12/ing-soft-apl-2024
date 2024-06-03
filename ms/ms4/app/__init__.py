from flask import Flask
from flask_marshmallow import Marshmallow
import os
from flask_caching import Cache
from app.config import config

ma = Marshmallow()
cache = Cache()
def create_app() -> None:
    app_context = os.getenv('FLASK_CONTEXT')
    app = Flask(__name__)
    f = config.factory(app_context if app_context else 'development')
    app.config.from_object(f)

    ma.init_app(app)
    cache.init_app(app, config={'CACHE_TYPE':'RedisCache', 
                                'CACHE_DEFAULT_TIMEOUT':300,
                                'CACHE_REDIS_HOST':'localhost', 
                                'CACHE_REDIS_PORT':'6379', 
                                'CACHE_REDIS_DB':'0', 
                                'CACHE_REDIS_PASSWORD':'Qvv3r7y',
                                'CACHE_KEY_PREFIX':'orquestador_'})
    from app.resources import home
    app.register_blueprint(home, url_prefix='/api/v1')
    
    
    @app.shell_context_processor    
    def ctx():
        return {"app": app}
    
    return app
