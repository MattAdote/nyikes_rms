# project specific imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# set reference to sqlalchemy
db = SQLAlchemy()

# set reference to Marshmallow
ma = Marshmallow()

# local imports
from instance.config import app_config

from app.api.v1.views import    default_view_blueprint, superusers_view_blueprint, \
                                settings_config_members_view_blueprint, members_view_blueprint

def create_api_server(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.register_blueprint(default_view_blueprint, url_prefix='/api/v1')
    app.register_blueprint(superusers_view_blueprint, url_prefix='/api/v1')
    app.register_blueprint(settings_config_members_view_blueprint, url_prefix='/api/v1')
    app.register_blueprint(members_view_blueprint, url_prefix='/api/v1')

    # Initialize SQLAlchemy 
    db.init_app(app)
    
    # initialize Marshmallow
    ma.init_app(app)

    return app
