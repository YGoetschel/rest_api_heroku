from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')  # lazy=dynamic turns Items into a query builder

    def __init__(self, name):
        self.name = name

    def json(self):
        return {"name": self.name, "items": [item.json() for item in self.items.all()]}  # list comprehension to get all items for given store

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  # query = SQLAlchemy query builder
    # above line = SELECT top(1) * FROM stores where name = name (variable) then converts output to model object

    def save_to_db(self):
        db.session.add(self)  # session = collection of objects to write to db
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


