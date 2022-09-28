from flask import Blueprint, render_template, url_for, flash
from app.models import Pelanggan
from flask_login import current_user, login_required

bp = Blueprint('pelanggan', __name__)

@bp.route('/<int:id>')
@login_required
def show(id):
    pelanggan = Pelanggan.get(id)
    return render_template('pelanggan/show.html', pelanggan=pelanggan)

@bp.route('/')
@login_required
def index():
    
    users = Pelanggan.select()
    return render_template('pelanggan/index.html', users=users)