from flask_restful import Resource, reqparse
from app.models.user import UserModel

class User(Resource):
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

        if (user := UserModel.find_by_username(data['username'])):
            print('user', user)
            return {'message': "User found"}, 200

        return {'message': 'User not found.'}, 404

    def post(self):
        data = self.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': "A user with that username is already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'User created successfully.'}, 201
