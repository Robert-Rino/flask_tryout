import datetime

from flask import make_response, jsonify, make_response
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


from app.models.user import User

class LoginResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
    type=str,
    required=True,
    help='This field cannot be blank !')

    parser.add_argument('password',
    type=str,
    # required=True,
    help='This field cannot be blank !')

    def post(self):
        data = self.parser.parse_args()
        if user := User.find(username=data['username'], password=data['password']):
            now = datetime.datetime.utcnow()
            access_token = create_access_token(
                identity=user.id,
                headers={
                    'nbf': now,
                    'exp': now + datetime.timedelta(days=14)
                }
            )
            response = make_response({
                'access_token': access_token
            })
            response.headers['access_token'] = access_token
            return response

    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        return make_response({
            'user_id': user_id
        })
