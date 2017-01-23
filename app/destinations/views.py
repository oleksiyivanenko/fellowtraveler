from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_required, current_user

from app import db
from app.destinations.models import Destination, Comment

destinations = Blueprint('destinations', __name__)


@destinations.route('/')
@login_required
def records():
    dests = Destination.query.all()
    return render_template(
        'destinations/records.html',
        dests=dests,
        current_user=current_user,
    )


@destinations.route('/destinations/<int:destination_id>')
@login_required
def show(destination_id):
    dest = Destination.query.filter_by(id=destination_id).first_or_404()
    return render_template('destinations/show.html', dest=dest)


@destinations.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'GET':
        return render_template(
            'destinations/add.html',
            current_user=current_user
        )

    destination = Destination(
        city=request.form['city'],
        country=request.form['country'],
        photo=request.form['photo'],
        description=request.form['description'],
        created_by=current_user.name,
        updated_by=current_user.name,
    )

    destination.users.append(current_user)

    db.session.add(destination)
    db.session.commit()

    return redirect(url_for('destinations.records'))


@destinations.route('/comments/add', methods=['POST'])
@login_required
def comment_add():
    comment = Comment(
        destination_id=int(request.form['destination_id']),
        text=request.form['new_comment'],
        created_by=current_user.name,
        updated_by=current_user.name,
    )
    db.session.add(comment)
    db.session.commit()

    return redirect(url_for(
        'destinations.show',
        destination_id=request.form['destination_id']
    ))
