from flask import Blueprint
from flask_restx import Api
from .resources.courses import api as courses_api

api_blueprint = Blueprint("api", __name__, url_prefix='/api/1.0')
api = Api(
    api_blueprint,
    title='Courses main api',
    version='1.0',
    default_label='CRUD operations with courses',
    default='Courses'
)
api.add_namespace(courses_api)
