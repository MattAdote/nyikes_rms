import os


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    

class DevelopmentConfig(Config):
    """Configurations for Development."""
    ENV = 'development'
    DEBUG = True
    ACTIVATION_TOKEN_EXPIRY_SECONDS = 300

class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    ENV = 'testing'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')
    MAIL_SUPPRESS_SEND = False
    ACTIVATION_TOKEN_EXPIRY_SECONDS = 1

class StagingConfig(Config):
    """Configurations for Staging."""
    ENV = 'staging'
    DEBUG = True
    ACTIVATION_TOKEN_EXPIRY_SECONDS = 360

class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False
    ACTIVATION_TOKEN_EXPIRY_SECONDS = 604800

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}

# Email server config settings
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
# admin email list
ADMINS =[
    'info@nyikes.org',
    'ianad.devtest@gmail.com'
]