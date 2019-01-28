from flask import Flask

# local import
from instance.config import app_config

from app.api.v1.views import default_view_blueprint

def create_api_server(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    
    app.register_blueprint(default_view_blueprint, url_prefix='/api/v1')

    return app