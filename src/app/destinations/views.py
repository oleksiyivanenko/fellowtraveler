from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_required, current_user

from app import db
from app.auth.models import User
from app.destinations.models import Destination, Comment
from app.destinations.forms import CommentForm, DestinationForm

destinations = Blueprint('destinations', __name__)


@destinations.route('/')
@login_required
def records():
    dests = current_user.destinations
    if request.args.get('all') is None:
        dests = filter(lambda x: not x.is_completed, dests)
    return render_template(
        'destinations/records.html',
        dests=dests,
        current_user=current_user,
    )


@destinations.route('/destinations/<int:destination_id>')
@login_required
def show(destination_id):
    dest = Destination.query.filter_by(id=destination_id).filter(
        Destination.users.any(id=current_user.id)
    ).first_or_404()
    form = CommentForm(destination_id=dest.id)
    return render_template('destinations/show.html', dest=dest, form=form)


@destinations.route('/destinations/delete/<int:destination_id>')
@login_required
def delete(destination_id):
    dest = Destination.query.filter_by(id=destination_id).filter(
        Destination.users.any(id=current_user.id)
    ).first_or_404()

    db.session.delete(dest)
    db.session.commit()

    return redirect(url_for('destinations.records'))


@destinations.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = DestinationForm()
    travel_with = db.session.query(User).filter(
        User.id != current_user.id
    )
    form.traveling_with.choices = [(user.id, user.name) for user in travel_with]

    if form.validate_on_submit():
        destination = Destination(
            created_by=current_user.name,
            updated_by=current_user.name,
        )
        form.populate_obj(destination)

        destination.users.append(current_user)

        if form.traveling_with.data:
            travelers = db.session.query(User).filter(User.id.in_(
                form.traveling_with.data
            ))
            destination.users.extend(travelers)

        db.session.add(destination)
        db.session.commit()

        return redirect(url_for('destinations.records'))

    return render_template(
        'destinations/add.html',
        current_user=current_user,
        form=form,
    )


@destinations.route('/destinations/edit/<int:destination_id>', methods=['GET', 'POST'])
@login_required
def edit(destination_id):
    destination = Destination.query.filter_by(id=destination_id).filter(
        Destination.users.any(id=current_user.id)
    ).first_or_404()

    form = DestinationForm(obj=destination)
    travel_with = db.session.query(User).filter(
        User.id != current_user.id
    )
    form.traveling_with.choices = [(user.id, user.name) for user in travel_with]

    if form.validate_on_submit():
        form.populate_obj(destination)
        destination.updated_by = current_user.name

        destination.users.append(current_user)

        if form.traveling_with.data:
            travelers = db.session.query(User).filter(User.id.in_(
                form.traveling_with.data
            ))
            destination.users.extend(travelers)

        db.session.add(destination)
        db.session.commit()

        return redirect(url_for('destinations.show', destination_id=destination.id))

    return render_template(
        'destinations/edit.html',
        current_user=current_user,
        form=form,
    )


@destinations.route('/destinations/mark_completed/<int:destination_id>', methods=['GET'])
@login_required
def mark_completed(destination_id):
    destination = Destination.query.filter_by(id=destination_id).filter(
        Destination.users.any(id=current_user.id)
    ).first_or_404()
    destination.is_completed = True
    db.session.add(destination)
    db.session.commit()

    return redirect(url_for('destinations.records'))


@destinations.route('/comments/add', methods=['POST'])
@login_required
def comment_add():
    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment(
            created_by=current_user.name,
            updated_by=current_user.name,
        )

        form.populate_obj(comment)
        db.session.add(comment)
        db.session.commit()

        return redirect(url_for(
            'destinations.show',
            destination_id=request.form['destination_id']
        ))
