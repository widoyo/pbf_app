from flask import Blueprint, render_template, url_for, flash, redirect, abort
from flask_login import login_required, current_user
from app.models import User
from app.forms import UserForm

bp = Blueprint('user', __name__)


@bp.route('/add', methods=['POST', 'GET'])
@login_required
def add():
    if current_user.role != 0:
        abort(403)
    form = UserForm()
    errors = None
    if form.validate_on_submit():
        new_user, created = User.get_or_create(username=form.username.data, 
                                               role=form.role.data,
                                               password=form.password.data)
        new_user.set_password(form.password.data)
        new_user.save()
        flash('Sukses menambah %s'.format(new_user.username), 'success')
        return redirect(url_for('user.index'))
    else:
        errors = form.errors
    return render_template('user/add.html', form=form, errors=errors)

@bp.route('/')
def index():
    if current_user.role != 0:
        abort(403)
    users = User.select()
    return render_template('user/index.html', users=users)

