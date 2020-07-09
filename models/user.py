import sqlite3
from db import db


class UserModel(db.Model):
    # define related table name and columns from database
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)  # session = collection of objects to write to db
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
