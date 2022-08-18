from flask import Blueprint, render_template, url_for, flash
from app.models import Jual

bp = Blueprint('pesanan', __name__)

@bp.route('/')
def index():
    users = Pelanggan.select()
    return render_template('pesanan/index.html', users=users)