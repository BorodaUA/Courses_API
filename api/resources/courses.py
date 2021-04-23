from api.models.courses import CourseModel
from api.schemas.courses import CourseSchema
from flask import g, jsonify, make_response, request
from flask_restx import Namespace, Resource
from marshmallow import ValidationError

api = Namespace(name="", description="Courses API")
add_course_schema = CourseSchema(exclude=['id'])


@api.route('/courses')
class Courses(Resource):
    def get(self):
        '''
        Return message Hello World,
        to the GET request, on the /courses endpoint
        '''
        return {'message': 'Hello World'}, 200

    def post(self):
        '''
        Getting POST requests on the '/courses' endpoint, and
        saving new course to the database.
        '''
        try:
            course = add_course_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400
        db_session = g.session
        db_session.add(CourseModel(**course))
        db_session.commit()
        return make_response(
            jsonify(
                {
                    "message": "Course added",
                    "code": 201
                }
            ),
            201,
        )
