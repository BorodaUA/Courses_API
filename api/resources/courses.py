from flask_restx import Resource, Namespace

api = Namespace(name="", description="Courses API")


@api.route('/courses')
class Courses(Resource):
    def get(self):
        '''
        Return message Hello World,
        to the GET request, on the /courses endpoint
        '''
        return {'message': 'Hello World'}, 200
