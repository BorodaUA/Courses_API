from api.models.courses import CourseModel
from api.schemas.courses import CourseSchema, IdSchema
from flask import g, jsonify, make_response, request
from flask_restx import Namespace, Resource, fields
from marshmallow import ValidationError
from time import time

api = Namespace(name="", description="Courses API")
add_course_schema = CourseSchema(exclude=['id'])
list_courses_schema = CourseSchema(
    many=True,
)
id_schema = IdSchema()
get_course_schema = CourseSchema()

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
valid_response_model = api.model(
    'Course response model',
    {
        'id': fields.Integer(default=1),
        'name': fields.String(
            default=f"Example of the course name {time()}"
        ),
        'lectures_count': fields.Integer(default=11),
        'start_date': fields.Date(default='2021-05-17'),
        'end_date': fields.Date(default='2021-07-30')
    },
    description='Course object that will retrived from the database',
)
put_200_response_model = api.model(
    'PUT 200 response model',
    {
        "code": fields.Integer(default=200),
        "message": fields.String("Course updated")
    }
)


@api.route('/courses')
class Courses(Resource):
    def get(self):
        '''
        Getting GET requests on the '/courses' endpoint, and
        returning list of the courses from the database
        '''
        db_session = g.session
        courses = db_session.query(CourseModel).all()
        courses = list_courses_schema.dump(courses)
        return jsonify(courses)

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


@api.route('/courses/<int:id>')
@api.param(name='id', description='A course unique id', default=1)
class Course(Resource):
    @api.response(200, "Success", model=valid_response_model)
    def get(self, id):
        '''
        Getting GET requests on the /courses/<id> endpoint and
        return a course by id
        '''
        try:
            id = {"id": id}
            id = id_schema.load(id)
        except ValidationError as err:
            return err.messages, 400
        db_session = g.session
        course = db_session.query(CourseModel).filter_by(
            id=id['id']
        ).first()
        if not course:
            return make_response(
                jsonify(
                    {
                        "message": "Course not found",
                        "code": 404
                    }
                    ),
                404,
            )
        course = get_course_schema.dump(course)
        return jsonify(course)

    @api.expect(valid_request_model)
    @api.response(200, "Success", model=put_200_response_model)
    @api.response(201, "Success", model=success_msg)
    def put(self, id):
        '''
        Getting PUT requests on the /courses/<id> endpoint and
        updating information about a course, if it exists, or
        creating new record if it is not.
        '''
        try:
            id = {"id": id}
            id = id_schema.load(id)
        except ValidationError as err:
            return err.messages, 400
        try:
            course = add_course_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400
        db_session = g.session
        course_exist_by_id = db_session.query(CourseModel).filter(
            CourseModel.id == id['id']
        ).first()
        course_exist_by_name = db_session.query(CourseModel).filter(
            CourseModel.name == course["name"]
        ).first()
        # check if course exist by id
        if course_exist_by_id:
            # check if course exist by name
            if course_exist_by_name:
                # check if id and name belongs to the same course
                if course_exist_by_name.id != id["id"]:
                    return make_response(jsonify(
                        {
                            "message": (
                                "Bad request, course id and name mismatch"),
                            "code": 400
                        }
                    ), 400,)
                # updating course
                else:
                    db_session.query(CourseModel).filter(
                        CourseModel.id == id['id']
                    ).update(
                        {
                            "name": course["name"],
                            "lectures_count": course["lectures_count"],
                            "start_date": course["start_date"],
                            "end_date": course["end_date"]
                        }
                    )
                    db_session.commit()
                    return make_response(jsonify(
                        {
                            "message": "Course updated",
                            "code": 200
                        }
                    ), 200,)
            # updating course fields
            else:
                db_session.query(CourseModel).filter(
                    CourseModel.id == id['id']
                ).update(
                    {
                        "name": course["name"],
                        "lectures_count": course["lectures_count"],
                        "start_date": course["start_date"],
                        "end_date": course["end_date"]
                    }
                )
                db_session.commit()
                return make_response(jsonify(
                    {
                        "message": "Course updated",
                        "code": 200
                    }
                ), 200,)
        if not course_exist_by_id:
            # check if course name already exists
            if course_exist_by_name:
                return make_response(
                    jsonify(
                        {
                            "message": "Course with this name already exist"
                        }
                    ), 400
                )
            # adding course if it is new
            else:
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
