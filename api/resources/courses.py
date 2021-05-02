from api.models.courses import CourseModel
from api.schemas.courses import CourseSchema, IdSchema, CourseFilterSchema
from flask import g, jsonify, make_response, request
from flask_restx import Namespace, Resource, fields
from marshmallow import ValidationError
from time import time
import logging

api = Namespace(name="", description="Courses API")
add_course_schema = CourseSchema(exclude=['id'])
list_courses_schema = CourseSchema(
    many=True,
)
id_schema = IdSchema()
get_course_schema = CourseSchema()
course_filters_name_schema = CourseFilterSchema(
    exclude=['start_date', 'end_date']
)
course_filters_start_date_schema = CourseFilterSchema(
    exclude=['name', 'end_date']
)
course_filters_end_date_schema = CourseFilterSchema(
    exclude=['name', 'start_date']
)

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
delete_200_response_model = api.model(
    'DELETE 200 response model',
    {
        "code": fields.Integer(default=200),
        "message": fields.String("Course deleted")
    }
)
delete_404_response_model = api.model(
    'DELETE 200 response model',
    {
        "code": fields.Integer(default=404),
        "message": fields.String("Course not found")
    }
)


@api.route('/courses')
class Courses(Resource):
    @api.param(
        name='end_date',
        description='A course end_date',
        default='2021-07-30'
    )
    @api.param(
        name='start_date',
        description='A course start_date',
        default='2021-05-17'
    )
    @api.param(
        name='name',
        description='A course unique name',
        default='Example'
    )
    def get(self):
        '''
        Getting GET requests on the '/courses' endpoint, and
        returning list of the courses from the database if no parameters
        provided or filtering by course name, start_date, end_date
        '''
        incoming_name = {
            'name': request.args.get(
                'name',
                default=None,
                type=None
            )
        }
        incoming_start_date = {
            'start_date': request.args.get(
                'start_date',
                default=None,
                type=None
            )
        }
        incoming_end_date = {
            'end_date': request.args.get(
                'end_date',
                default=None,
                type=None
            )
        }
        # validating name
        try:
            incoming_name = course_filters_name_schema.load(
                incoming_name
            )
        except ValidationError as err:
            logging.debug(err)
            incoming_name = {'name': None}
        # validating start_date
        try:
            incoming_start_date = course_filters_start_date_schema.load(
                incoming_start_date
            )
        except ValidationError as err:
            logging.debug(err)
            incoming_start_date = {'start_date': None}
        # validating end_date
        try:
            incoming_end_date = course_filters_end_date_schema.load(
                incoming_end_date
            )
        except ValidationError as err:
            logging.debug(err)
            incoming_end_date = {'end_date': None}
        # get session
        db_session = g.session
        # if no query params, return all courses
        if (incoming_name['name'] is None and
                incoming_start_date['start_date'] is None and
                incoming_end_date['end_date'] is None):
            courses = db_session.query(CourseModel).all()
            courses = list_courses_schema.dump(courses)
            return jsonify(courses)
        # courses found by name
        courses_found_by_name = db_session.query(CourseModel).filter(
            CourseModel.name.like(f'%{incoming_name["name"]}%')
        )
        # courses found by start_date
        courses_found_by_start_date = db_session.query(CourseModel).filter(
            CourseModel.start_date == incoming_start_date["start_date"],
        )
        # courses found by end_date
        courses_found_by_end_date = db_session.query(CourseModel).filter(
            CourseModel.end_date == incoming_end_date["end_date"],
        )
        # combining the results
        combined_results = courses_found_by_name.union(
            courses_found_by_start_date,
            courses_found_by_end_date
        )
        combined_results = list_courses_schema.dump(
            combined_results
        )
        return jsonify(combined_results)

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

    @api.response(200, "Success", model=delete_200_response_model)
    @api.response(404, "Not Found", model=delete_404_response_model)
    def delete(self, id):
        '''
        Getting DELETE requests on the /courses/<id> endpoint and
        deleting a course from the database
        '''
        try:
            id = {"id": id}
            id = id_schema.load(id)
        except ValidationError as err:
            return err.messages, 400
        db_session = g.session
        course_exist_by_id = db_session.query(CourseModel).filter(
            CourseModel.id == id['id']
        ).first()
        if not course_exist_by_id:
            return make_response(
                jsonify({"message": "Course not found", "code": 404}), 404
            )
        db_session.query(CourseModel).filter(
            CourseModel.id == id['id']
        ).delete()
        db_session.commit()
        return make_response(jsonify(
            {
                "message": "Course deleted",
                "code": 200
            }
        ), 200,)
