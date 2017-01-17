from datetime import datetime

from app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    password = db.Column(db.String)
    email = db.Column(db.String, unique=True, index=True)
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % self.name
