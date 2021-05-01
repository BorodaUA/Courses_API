import pytest
import os
import sys
tests_folder_path = os.path.dirname(os.path.abspath(__file__)) + '/../'
sys.path.append(tests_folder_path)
from courses_crud import create_app # noqa


@pytest.fixture(scope='function')
def client(request):
    app = create_app(config_name="testing")
    with app.test_client() as client:
        yield client

        @app.teardown_appcontext
        def delete_test_db_file(exception=None):
            test_db_file_path = app.config['DATABASE_FILE_PATH']
            os.unlink(test_db_file_path)
