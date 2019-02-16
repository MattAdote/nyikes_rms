import os

from app import create_api_server

config_name = os.getenv('APP_SETTINGS')
api_server = create_api_server(config_name)

if __name__ == '__main__':
    api_server.run()