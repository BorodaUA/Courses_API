import json


def test_api_post_courses_valid_json_data(client):
    """
    Test POST /api/1.0/courses, add course, all fields valid
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


def test_api_post_courses_json_data_missing(client):
    """
    Test POST /api/1.0/courses, add course, all json data missing
    """
    response = client.post(
        "/api/1.0/courses",
    )
    response = json.loads(response.data)
    assert (
        {
            "_schema": ["Invalid input type."]
        }
    ) == response


def test_api_post_courses_json_data_empty(client):
    """
    Test POST /api/1.0/courses, add course, all json data empty
    """
    response = client.post(
        "/api/1.0/courses",
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
