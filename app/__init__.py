from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# local import
from instance.config import app_config

from app.api.v1.views import default_view_blueprint, superusers_view_blueprint

# initialize sqlalchemy
db = SQLAlchemy()

def create_api_server(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.register_blueprint(default_view_blueprint, url_prefix='/api/v1')
    app.register_blueprint(superusers_view_blueprint, url_prefix='/api/v1')

    # 
    db.init_app(app)

    return app