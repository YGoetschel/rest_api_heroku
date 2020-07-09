from flask import Flask
from flask_restful import Api
import yaml
import os
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, Items
from resources.store import Store, StoreList

# load yaml config file
with open(os.path.join(os.path.dirname(__file__), "config.yaml"), mode='r') as stream:
    keys = yaml.load(stream=stream, Loader=yaml.FullLoader)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  #db type: root folder of project
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = keys['secret_key']
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')


if __name__ == '__main__':
    from db import db  # Circular import
    db.init_app(app)
    app.run(port=5000)
