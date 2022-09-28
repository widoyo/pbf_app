from flask import Blueprint, render_template, url_for, flash
from flask_login import login_required
from app.models import Absen, Moving

from app.forms import AbsenForm

bp = Blueprint('absen', __name__)

@bp.route('/')
@login_required
def index():
    absens = Absen.select()
    return render_template('absen/index.html', absens=absens)

