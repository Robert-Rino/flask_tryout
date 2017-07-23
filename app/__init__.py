import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from app.resources.user import UserRegister
from app.resources.item import Item, ItemList
from app.resources.store import Store, StoreList

from config import config

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    api = Api(app)

    jwt = JWT(app, authenticate, identity) #/auth

    api.add_resource(Store, '/store/<string:name>')
    api.add_resource(Item, '/item/<string:name>')
    api.add_resource(ItemList, '/items')
    api.add_resource(StoreList, '/stores')
    api.add_resource(UserRegister, '/register')

    if app.config['DEBUG']:
        from db import db
        db.init_app(app)

        @app.before_first_request
        def create_tables():
            db.create_all()


    return app
