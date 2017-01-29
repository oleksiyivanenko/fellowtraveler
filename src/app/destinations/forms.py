import pycountry
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (
    HiddenField,
    SelectField,
    SelectMultipleField,
    StringField,
    TextAreaField,
)
from wtforms.validators import required, url

from app import db
from app.auth.models import User


def get_travelers_choices():
    return db.session.query(User).filter(User.id != current_user.id)


class DestinationForm(FlaskForm):
    country = SelectField(
        u'Country',
        validators=[required()],
        choices=[(country.name, country.name)
                 for country in pycountry.countries]
    )
    city = StringField(u'City', validators=[required()])

    photo = StringField(u'Photo url', validators=[url()])
    description = TextAreaField(u'Description')
    traveling_with = SelectMultipleField(
        u'I will travel with',
        coerce=int,
        choices=[]
    )


class CommentForm(FlaskForm):
    destination_id = HiddenField()
    text = TextAreaField(u'Comment', validators=[required()])
