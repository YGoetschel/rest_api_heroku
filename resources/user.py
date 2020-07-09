import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field connot be blank")
    parser.add_argument('password', type=str, required=True, help="This field connot be blank")

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            resp = {"message": "user: '{}' already exists".format(data['username'])}, 400
        else:
            user = UserModel(username=data['username'], password=data['password'])
            user.save_to_db()
            resp = {"message": "user: '{}' is created".format(data['username'])}, 201
        return resp

    def delete(self):
        data = UserRegister.parser.parse_args()
        user = UserModel.find_by_username(data["username"])
        if user:
            user.delete_from_db()
            resp = {"message": "user '{}' Deleted".format(data['username'])}
        else:
            resp = {"message": "user '{}' Not Found".format(data['username'])}
        return resp
