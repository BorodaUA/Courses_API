import json
from conftest import add_course


def test_api_get_courses_empty_table(client):
    """
    Test GET /api/1.0/courses, empty table, no courses
    """
    response = client.get("/api/1.0/courses")
    response = json.loads(response.data)
    assert [] == response


def test_api_get_courses_course_added(client):
    """
    Test GET /api/1.0/courses, a course added to the table
    """
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
    response = client.get("/api/1.0/courses")
    response = json.loads(response.data)
    assert [
        {
            'id': 1,
            'name': test_user_data['title'],
            'lectures_count': test_user_data['lectures_count'],
            'start_date': test_user_data['start_date'],
            'end_date': test_user_data['end_date'],
        }
    ] == response


def test_api_get_courses_search_by_name(client):
    """
    Test GET /api/1.0/courses?name="course name"
    courses added to the table
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
    response = client.get(f"/api/1.0/courses?name={test_user_data['title']}")
    response = json.loads(response.data)
    assert [
        {
            'id': 11,
            'name': test_user_data['title'],
            'lectures_count': test_user_data['lectures_count'],
            'start_date': test_user_data['start_date'],
            'end_date': test_user_data['end_date'],
        }
    ] == response


def test_api_get_courses_search_by_start_date(client):
    """
    Test GET /api/1.0/courses?start_date="start date"
    courses added to the table
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
        f"/api/1.0/courses?start_date={test_user_data['start_date']}"
    )
    response = json.loads(response.data)
    assert [
        {
            'id': 11,
            'name': test_user_data['title'],
            'lectures_count': test_user_data['lectures_count'],
            'start_date': test_user_data['start_date'],
            'end_date': test_user_data['end_date'],
        }
    ] == response


def test_api_get_courses_search_by_end_date(client):
    """
    Test GET /api/1.0/courses?end_date="end date"
    courses added to the table
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
        f"/api/1.0/courses?end_date={test_user_data['end_date']}"
    )
    response = json.loads(response.data)
    assert [
        {
            'id': 11,
            'name': test_user_data['title'],
            'lectures_count': test_user_data['lectures_count'],
            'start_date': test_user_data['start_date'],
            'end_date': test_user_data['end_date'],
        }
    ] == response
