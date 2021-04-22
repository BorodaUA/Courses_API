from flask import Flask
from config import config
from api.api_bp import api_blueprint


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.register_blueprint(api_blueprint)
    return app
