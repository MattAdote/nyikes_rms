# python imports
import os
from flask_script import Manager 
from flask_migrate import Migrate, MigrateCommand

# local imports
from app import db, create_api_server
from app.api.v1.models.sa_models import * # import models


app = create_api_server(config_name=os.getenv('APP_SETTINGS'))
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
