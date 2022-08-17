from flask import Blueprint, render_template, url_for, flash
from app.models import User

bp = Blueprint('user', __name__)

@bp.route('/')
def index():
    users = User.select()
    return render_template('user/index.html', users=users)