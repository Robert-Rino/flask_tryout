import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
    type = float,
    required = True,
    help = 'This field cannot be blank !')

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name) #'self' here means Item class

        if item:
            return item, 200
        return {'message': 'item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()

        connection.close()

        if row:
            return {'item': {'name':row[0], 'price':row[1]}}


    def post(self, name):
        if Item.find_by_name(name):
            return {'message': 'An item with name {} already exists.'.format(name)}, 400
        data = Item.parser.parse_args()
        item = {
        'name': name,
        'price': data['price']
        }
        try:
            self.insert(item)
        except:
            return {'message':'An error occured when inserting data' }, 500
        return item, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        insert_row = "INSERT INTO items VALUES(?, ?)"
        cursor.execute(insert_row, (item['name'], item['price']))

        connection.commit()
        connection.close()


    def delete(self, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        insert_row = "DELETE FROM items WHERE name=?"
        cursor.execute(insert_row, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = self.find_by_name(name)
        updated_item = {"name": name, "price": data["price"]}

        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {'message': 'An error occured when insert item.'}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {'message': 'An error occured when update item.'}, 500
        return updated_item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        insert_row = "UPDATE items SET price = ? WHERE name = ?"
        cursor.execute(insert_row, (item['price'], item['name']))

        connection.commit()
        connection.close()

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = 'SELECT * FROM items'
        result = cursor.execute(query)

        items = []
        for row in result:
            items.append({"name":row[0], "price":row[1]})

        connection.close()
        return {'items':items}
