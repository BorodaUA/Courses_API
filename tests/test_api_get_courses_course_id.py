import json
from conftest import add_course


def test_api_get_course_by_id(client):
    """
    Test GET /api/1.0/courses/<id>, get course by id
    """
    add_course(client=client, times=10)
    test_user_data = client.application.config['test_data']
    response = client.post(
        "/api/1.0/courses",
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
    response = client.get(
        "/api/1.0/courses/11"
    )
    response = json.loads(response.data)
    assert (
        {
            'id': 11,
            'name': test_user_data['title'],
            'lectures_count': test_user_data['lectures_count'],
            'start_date': test_user_data['start_date'],
            'end_date': test_user_data['end_date'],
        }
    ) == response


def test_api_get_course_by_id_not_integer(client):
    """
    Test GET /api/1.0/courses/<id>, get course by id
    id not valid integer
    """
    add_course(client=client, times=10)
    response = client.get(
        "/api/1.0/courses/not_int"
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


def test_api_get_course_by_id_course_not_found(client):
    """
    Test GET /api/1.0/courses/<id>, get course by id
    course <id> not found
    """
    add_course(client=client, times=10)
    response = client.get(
        "/api/1.0/courses/20"
    )
    response = json.loads(response.data)
    assert (
        {
            'code': 404,
            'message': 'Course not found'
        }
    ) == response
