# -*- coding: utf-8 -*-
from flask_restful import Resource
from app.models.store import Store

class StoreResource(Resource):
    def get(self, name):
        store = Store.find_by_name(name)

        if store:
            return store.json(), 200
        return {'message': 'store not found'}, 404

    def post(self, name):
        if Store.find_by_name(name):
            return {'message': 'An store with name {} already exists.'.format(name)}, 400

        store = Store(name)

        try:
            store.save_to_db()
        except:
            return {'message':'An error occured when inserting data'}, 500
        return store.json(), 201

    def delete(self, name):
        store = Store.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': 'Store deleted'}
        else:
            return {'message': 'Store not found'}


class StoreList(Resource):
    def get(self):
        stores = Store.query.all()
        result = [store.json() for store in stores]
        return {'stores':result}
