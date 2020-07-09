from flask_restful import reqparse, Resource
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        resp = {"message": "store: '{}' Not found".format(name)}, 404
        store = StoreModel.find_by_name(name=name)
        if store:
            resp = store.json(), 200
        return resp

    def post(self, name):
        if StoreModel.find_by_name(name=name):
            resp = {"message": "Store: '{}' already exists".format(name)},  400
        else:
            store = StoreModel(name=name)
            store.save_to_db()
            resp = store.json(), 201
        return resp

    def delete(self, name):
        resp = {"message": "store: '{}' Not found".format(name)}, 404
        store = StoreModel.find_by_name(name=name)
        if store:
            store.delete_from_db()
            resp = {"message": "store: '{}' Deleted".format(name)}, 404
        return resp


class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.query.all()]}
