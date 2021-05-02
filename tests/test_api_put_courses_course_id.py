import json
from conftest import add_course


def test_api_put_course_by_id_valid_json_data(client):
    """
    Test PUT /api/1.0/courses/<id>, update course by id
    valid json data
    """
    add_course(client=client, times=10)
    test_user_data = client.application.config['test_data']
    response = client.put(
        "/api/1.0/courses/10",
        data=json.dumps(
            {
                'name': test_user_data['title'],
                'lectures_count': test_user_data['lectures_count'],
                'start_date': test_user_data['start_date'],
                'end_date': test_user_data['end_date'],
            }
        ),
        content_type="application/json",
    )
    response = json.loads(response.data)
    assert (
        {
            'code': 200,
            'message': 'Course updated'
        }
    ) == response


def test_api_put_course_by_id_json_data_missing(client):
    """
    Test PUT /api/1.0/courses/<id>, update course by id
    json data missing
    """
    add_course(client=client, times=10)
    response = client.put(
        "/api/1.0/courses/10",
    )
    response = json.loads(response.data)
    assert (
        {
            "_schema": ["Invalid input type."]
        }
    ) == response


def test_api_put_course_by_id_json_data_empty(client):
    """
    Test PUT /api/1.0/courses/<id>, update course by id
    empty json data
    """
    add_course(client=client, times=10)
    response = client.put(
        "/api/1.0/courses/10",
        data=json.dumps(
            {
                'name': '',
                'lectures_count': 0,
                'start_date': '',
                'end_date': '',
            }
        ),
        content_type="application/json",
    )
    response = json.loads(response.data)
    assert (
        {
            "name": [
                "Course name must be at least 2 symbols long."
            ],
            "end_date": [
                "Not a valid date."
            ],
            "lectures_count": [
                "Value must be greater than 0"
            ],
            "start_date": [
                "Not a valid date."
            ]
        }
    ) == response


def test_api_put_course_by_id_course_id_not_found(client):
    """
    Test PUT /api/1.0/courses/<id>, update course by id
    course <id> not found, adding new course
    """
    add_course(client=client, times=10)
    test_user_data = client.application.config['test_data']
    response = client.put(
        "/api/1.0/courses/20",
        data=json.dumps(
            {
                'name': test_user_data['title'],
                'lectures_count': test_user_data['lectures_count'],
                'start_date': test_user_data['start_date'],
                'end_date': test_user_data['end_date'],
            }
        ),
        content_type="application/json",
    )
    response = json.loads(response.data)
    assert (
        {
            'code': 201,
            'message': 'Course added'
        }
    ) == response


def test_api_put_course_by_id_course_id_not_integer(client):
    """
    Test PUT /api/1.0/courses/<id>, update course by id
    course <id> not valid integer
    """
    add_course(client=client, times=10)
    test_user_data = client.application.config['test_data']
    response = client.put(
        "/api/1.0/courses/not_int",
        data=json.dumps(
            {
                'name': test_user_data['title'],
                'lectures_count': test_user_data['lectures_count'],
                'start_date': test_user_data['start_date'],
                'end_date': test_user_data['end_date'],
            }
        ),
        content_type="application/json",
    )
    error_response = (
        b'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n'
        b'<title>404 Not Found</title>\n'
        b'<h1>Not Found</h1>\n'
        b'<p>The requested URL was not found on the server. '
        b'If you entered the URL manually please check your '
        b'spelling and try again.</p>\n'
    )
    assert error_response == response.data


def test_api_put_course_by_id_updating_course_name_with_existing_name(client):
    """
    Test PUT /api/1.0/courses/<id>, update course by id
    updating course name, with others existing course name
    """
    add_course(client=client, times=10)
    response = client.get(
        "/api/1.0/courses/9"
    )
    response = json.loads(response.data)
    existing_course_name = response['name']
    test_user_data = client.application.config['test_data']
    response = client.put(
        "/api/1.0/courses/10",
        data=json.dumps(
            {
                'name': existing_course_name,
                'lectures_count': test_user_data['lectures_count'],
                'start_date': test_user_data['start_date'],
                'end_date': test_user_data['end_date'],
            }
        ),
        content_type="application/json",
    )
    response = json.loads(response.data)
    assert (
        {
            'code': 400,
            'message': 'Bad request, course id and name mismatch'
        }
    ) == response
