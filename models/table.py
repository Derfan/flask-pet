from db import db


class TableModel(db.Model):
    __tablename__ = 'tables'

    id = db.Column(db.Integer, primary_key=True)
    seats = db.Column(db.Integer)

    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    restaurant = db.relationship('RestaurantModel')

    def __init__(self, seats, restaurant_id):
        self.seats = seats
        self.restaurant_id = restaurant_id

    def json(self):
        return {'restaurant_id': self.restaurant_id, 'seats': self.seats}

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.get(_id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
