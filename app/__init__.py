# project specific imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_mail import Mail

# Set references to some of the extensions used
# These must appear before the local imports 
# defined below so as to avoid ImportError
db = SQLAlchemy()
ma = Marshmallow()
mail = Mail()

# local imports
from instance.config import app_config, ADMINS

from app.api.v1.views import    default_view_blueprint, superusers_view_blueprint, \
                                settings_config_members_view_blueprint, members_view_blueprint

TEMPLATES_FOLDER = 'api/v1/views/templates'

def create_api_server(config_name):
    app = Flask(__name__, instance_relative_config=True, template_folder=TEMPLATES_FOLDER)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    app.config['ADMIN_EMAILS'] = ADMINS

    app.register_blueprint(default_view_blueprint, url_prefix='/api/v1')
    app.register_blueprint(superusers_view_blueprint, url_prefix='/api/v1')
    app.register_blueprint(settings_config_members_view_blueprint, url_prefix='/api/v1')
    app.register_blueprint(members_view_blueprint, url_prefix='/api/v1')

    # Initialize SQLAlchemy 
    db.init_app(app)
    
    # initialize Marshmallow
    ma.init_app(app)
    
    # initialize Flask-Mail
    mail.init_app(app)

    return app
