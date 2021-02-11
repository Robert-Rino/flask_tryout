# -*- coding: utf-8 -*-
import os

from flask import Flask, jsonify, make_response
from flask_restful import Api as _Api
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token,
    get_jwt_identity, exceptions)

from app.security import authenticate, identity
from app.models import db

from . import config


class Api(_Api):
    # REF: https://github.com/vimalloc/flask-jwt-extended/issues/141
    def error_router(self, original_handler, e):
        return original_handler(e)

def create_app():
    app = Flask(__name__)
    app.config.from_object(config.config.get(os.getenv('FLASK_CONFIG') or 'default'))
    api = Api(app)

    jwt = JWTManager(app) # auth

    @app.errorhandler(exceptions.NoAuthorizationError)
    @app.errorhandler(exceptions.JWTDecodeError)
    def auth_error(error):
        return {'code': 'AUTH_ERROR'}, 401


    from app.resources import user, login, article

    api.add_resource(user.UserResource, '/user')
    api.add_resource(login.LoginResource, '/login')
    api.add_resource(
        article.ArticleResource,
        '/article',
        '/article/<int:article_id>'
    )

    @app.route('/', endpoint='health_check')
    def health_check():
        return 'ok'

    @app.route('/.well-known/pki-validation/2A1E66F75F4AB6CDB31755C18B8FF515.txt')
    def wellknown():
        with open('statics/wellknown.txt') as f:
            return make_response(f.read())

    db.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()


    return app
