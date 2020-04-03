from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_key(cls, key, value):
        if key == 'login':
            return cls.query.filter_by(login=value).first()
        else:
            return cls.query.get(value)
