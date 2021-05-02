import json
from conftest import add_course
import random


def test_api_delete_course_by_id_valid_id(client):
    """
    Test DELETE /api/1.0/courses/<id>, delete course by id
    course <id> valid integer
    """
    add_course(client=client, times=10)
    response = client.delete(
        f"/api/1.0/courses/{random.randrange(1, 10)}"
    )
    response = json.loads(response.data)
    assert (
        {
            'code': 200,
            'message': 'Course deleted'
        }
    ) == response


def test_api_delete_course_by_id_course_not_found(client):
    """
    Test DELETE /api/1.0/courses/<id>, delete course by id
    course <id> not found
    """
    add_course(client=client, times=10)
    response = client.delete(
        "/api/1.0/courses/20"
    )
    response = json.loads(response.data)
    assert (
        {
            'code': 404,
            'message': 'Course not found'
        }
    ) == response


def test_api_delete_course_by_id_not_integer(client):
    """
    Test DELETE /api/1.0/courses/<id>, delete course by id
    course <id> not integer
    """
    add_course(client=client, times=10)
    response = client.delete(
        "/api/1.0/courses/im_not_an_integer"
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
