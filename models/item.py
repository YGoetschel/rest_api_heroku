from db import db

class ItemModel(db.Model):  # tells SQLAlchemy that we are going to save something
    # define related table name and columns from database
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)  # will not be used as now
    name = db.Column(db.String(100))
    price = db.Column(db.Float(precision=2))  # precision= nb de decimal places
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))  # foreign key= field in one table that refers to PK in other table

    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  # query = SQLAlchemy query builder
# above line = SELECT top(1) * FROM items where name = name (variable) then converts output to model object

    def save_to_db(self):
        db.session.add(self)  # session = collection of objects to write to db
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
