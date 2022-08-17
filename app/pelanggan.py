from flask import Blueprint, render_template, url_for, flash
from app.models import Pelanggan

bp = Blueprint('pelanggan', __name__)

@bp.route('/')
def index():
    users = Pelanggan.select()
    return render_template('pelanggan/index.html', users=users)