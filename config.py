import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):

    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard to guess string"
    DATABASE_FILE_PATH = os.environ.get("DATABASE_FILE_PATH")
    DATABASE_URI = os.environ.get("DATABASE_URI")


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    ENV = "development"


config = {
    "development": DevelopmentConfig,
}
