from flask_restful import reqparse, Resource
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()  # belong to class itself
    parser.add_argument('price', type=float, required=True, help='This field cannot be blank')
    parser.add_argument('store_id', type=int, required=True, help='Every Item need a store id')

    @jwt_required()  # have to authenticate before performing get method
    def get(self, name):
        data = ItemModel.find_by_name(name)  # return itemModel object
        if data:
            resp = data.json()
        else:
            resp = {"message": "item: '{}' not found".format(name)}
        return resp

    def post(self, name):
        if ItemModel.find_by_name(name):
            resp = {'message': 'item {} already exists'.format(name)}, 400
        else:
            data = Item.parser.parse_args()
            item = ItemModel(name=name, price=data['price'], store_id=data['store_id'])  # item is ItemModel Object
            try:
                item.save_to_db()
                resp = item.json(), 201
            except:
                resp = {"message": "error ocurred while insert item."}, 500
        return resp

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message": "item '{}' deleted".format(name)}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name=name, price=data['price'], store_id=data['store_id'])
        else:
            item.price = data['price']
            item.store_id = data['store_id']
        item.save_to_db()
        return item.json()


class Items(Resource):
    def get(self):
        return {"item": [item.json() for item in ItemModel.query.all()]}

