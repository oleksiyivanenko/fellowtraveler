from flask import Blueprint
from flask_login import login_required, current_user

from app.destinations.models import Destination

destinations = Blueprint('destinations', __name__)


@destinations.route('/list')
@login_required
def list():
    return current_user.name
    # dests = Destination.query.all()
    # return ', '.join([dest.city for dest in dests])
