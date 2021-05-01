import json


def test_api_get_courses(client):
    """
    Test GET /api/1.0/courses, empty database, no courses
    """
    response = client.get("/api/1.0/courses")
    response = json.loads(response.data)
    assert [] == response
