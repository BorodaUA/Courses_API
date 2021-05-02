from flask import Flask, g
from config import config
from api.api_bp import api_blueprint
from db import create_session_and_engine, create_db_file, Base


def create_app(config_name):
    app = Flask(__name__)
    #
    app.config.from_object(config[config_name])
    #
    app.register_blueprint(api_blueprint)
    #
    with app.app_context():
        create_db_file(app.config['DATABASE_FILE_PATH'])
    #
    engine_and_session = create_session_and_engine(
        app.config['DATABASE_URI']
    )
    session = engine_and_session['session']
    engine = engine_and_session['engine']

    @app.before_first_request
    def create_tables():
        Base.metadata.create_all(engine)

    @app.before_request
    def pass_session():
        g.session = session

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        if g.session:
            g.session.remove()

    return app
