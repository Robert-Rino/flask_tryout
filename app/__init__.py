# -*- coding: utf-8 -*-
import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from app.security import authenticate, identity
from app.resources.user import User
from app.resources.item import Item, ItemList
from app.resources.store import Store, StoreList

from config import config
from app.models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(config.get(os.getenv('FLASK_CONFIG') or 'default'))
    api = Api(app)

    jwt = JWT(app, authenticate, identity) #/auth

    api.add_resource(Store, '/store/<string:name>')
    api.add_resource(Item, '/item/<string:name>')
    api.add_resource(ItemList, '/items')
    api.add_resource(StoreList, '/stores')
    api.add_resource(User, '/user')

    @app.route('/', endpoint='health_check')
    def health_check():
        return 'ok'

    db.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()


    return app
