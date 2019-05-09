# project specific imports
from sqlalchemy import MetaData

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect

# for SQLAlchemy
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=convention)
# Set references to some of the extensions used
# These must appear before the local imports 
# defined below so as to avoid ImportError
db = SQLAlchemy(metadata=metadata)
ma = Marshmallow()
mail = Mail()
csrf = CSRFProtect()

# local imports
from instance.config import app_config, ADMINS

from app.api.v1.views import    default_view_blueprint, superusers_view_blueprint, \
                                settings_config_members_view_blueprint, members_view_blueprint

# constant for location of templates folder
# when using render_template()
TEMPLATES_FOLDER = 'api/v1/views/templates'

def create_api_server(config_name):
    app = Flask(__name__, instance_relative_config=True, template_folder=TEMPLATES_FOLDER)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    app.config['WTF_CSRF_SECRET_KEY'] = app.config['SECRET']
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['WTF_CSRF_CHECK_DEFAULT '] = False


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
    
    # initialize CSRF protection
    csrf.init_app(app)

    return app
