from flask import Blueprint, render_template, url_for, flash
from app.models import Obat

bp = Blueprint('obat', __name__)

@bp.route('/')
def index():
    obats = Obat.select()
    return render_template('obat/index.html', obats=obats)