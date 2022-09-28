from flask import Blueprint, render_template, url_for, flash
from flask_login import login_required, current_user
from app.models import Jual, Obat
from app.forms import PesananInForm

bp = Blueprint('penjualan', __name__)

@bp.route('/<int:id>')
@login_required
def show(id):
    jual = Jual.get(id)
    return render_template('penjualan/show.html', jual=jual, obats=Obat.select().order_by(Obat.nama))


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = PesananInForm()
    if form.validate_on_submit():
        print(form.pelanggan.data)
    juals = Jual.select().order_by(Jual.tanggal.asc())
    return render_template('penjualan/index.html', penjualan=juals)