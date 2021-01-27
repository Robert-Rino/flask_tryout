from flask import make_response
from flask_restful import Resource, reqparse
from app.models.user import User

class UserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
    type=str,
    required=True,
    help='This field cannot be blank !')

    parser.add_argument('password',
    type=str,
    # required=True,
    help='This field cannot be blank !')

    def get(self):
        data = self.parser.parse_args()
        print('data', data)

        if (user := User.find_by_username(data['username'])):
            return {
                'message': user.username,
            }

        return {'message': 'User not found.'}, 404

    def post(self):
        data = self.parser.parse_args()

        if User.find_by_username(data['username']):
            return {'message': "A user with that username is already exists"}, 400

        user = User(**data)
        user.save_to_db()

        return {'message': 'User created successfully.'}, 201
