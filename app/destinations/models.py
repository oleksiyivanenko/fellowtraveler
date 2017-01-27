import datetime

from app import db


UsersDestinations = db.Table('usersdestinations',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('destination_id', db.Integer, db.ForeignKey('destinations.id'))
)


class Destination(db.Model):
    __tablename__ = 'destinations'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer)
    order = db.Column(db.Integer)

    photo = db.Column(db.String)

    description = db.Column(db.Text)

    is_completed = db.Column(db.Boolean, nullable=False, default=False)

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow,
                           onupdate=datetime.datetime.utcnow)
    created_by = db.Column(db.String)
    updated_by = db.Column(db.String)

    comments = db.relationship('Comment', backref='destination',
                               order_by="desc(Comment.created_at)")
    users = db.relationship('User', secondary=UsersDestinations,
                            backref=db.backref('destinations'))


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'))
    text = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow,
                           onupdate=datetime.datetime.utcnow)
    created_by = db.Column(db.String)
    updated_by = db.Column(db.String)
