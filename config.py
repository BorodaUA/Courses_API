import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):

    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard to guess string"


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    ENV = "development"


config = {
    "development": DevelopmentConfig,
}
