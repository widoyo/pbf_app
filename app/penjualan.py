from flask import Blueprint, render_template, url_for, flash
from flask_login import login_required, current_user
from app.models import Jual

bp = Blueprint('penjualan', __name__)

@bp.route('/')
@login_required
def index():
    juals = Jual.select().where(Jual.sales.Jual.status == 9)
    return render_template('penjualan/index.html', users=users)