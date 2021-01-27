# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from app.models.item import Item

class ItemResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
    type = float,
    required = True,
    help = 'This field cannot be blank !')

    parser.add_argument('store_id',
    type = int,
    required = True,
    help = 'Item must belongs to a store !')

    @jwt_required()
    def get(self, name):
        item = Item.find_by_name(name) #'self' here means Item class

        if item:
            return item.json(), 200
        return {'message': 'item not found'}, 404

    def post(self, name):
        if Item.find_by_name(name):
            return {'message': 'An item with name {} already exists.'.format(name)}, 400
        data = Item.parser.parse_args()
        item = Item(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {'message':'An error occured when inserting data' }, 500
        return item.json(), 201

    def delete(self, name):
        item = Item.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted'}
        else:
            return {'message': 'Item not found'}


    def put(self, name):
        data = ItemResource.parser.parse_args()
        item = Item.find_by_name(name)

        if item:
            item.price = data['price']
        else:
            item = Item(name, data['price'], data['store_id'])

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        items = Item.query.all()
        result = [item.json() for item in items]
        return {'items':result}
