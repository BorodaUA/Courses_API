from api.models.courses import CourseModel
from api.schemas.courses import CourseSchema
from flask import g, jsonify, make_response, request
from flask_restx import Namespace, Resource, fields
from marshmallow import ValidationError
from time import time

api = Namespace(name="", description="Courses API")
add_course_schema = CourseSchema(exclude=['id'])

valid_request_model = api.model(
    'Course',
    {
        'name': fields.String(
            default=f"Example of the course name {time()}"
        ),
        'lectures_count': fields.Integer(default=11),
        'start_date': fields.Date(default='2021-05-17'),
        'end_date': fields.Date(default='2021-07-30')
    },
    description='Course object that will be added to the database',
)
success_msg = api.model(
    'success_msg',
    {
        "code": fields.Integer(default=201),
        "message": fields.String(default="Course added")
    }
)
duplicate_msg = api.model(
    'duplicate_msg',
    {
        "message": fields.String(
            default="Course with this name already exist"
        )
    }
)


@api.route('/courses')
class Courses(Resource):
    def get(self):
        '''
        Return message Hello World,
        to the GET request, on the /courses endpoint
        '''
        return {'message': 'Hello World'}, 200

    @api.expect(valid_request_model)
    @api.response(201, "Success", model=success_msg)
    @api.response(400, "Bad request", model=duplicate_msg)
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
        course_name_exist = db_session.query(CourseModel).filter_by(
            name=course["name"]
        ).first()
        if course_name_exist:
            return make_response(
                jsonify(
                    {
                        "message": "Course with this name already exist"
                    }
                ), 400
            )
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
