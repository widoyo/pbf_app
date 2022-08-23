from flask import jsonify, request
from playhouse.flask_utils import get_object_or_404
from flask_login import login_required
from app.api import bp
from app.models import Pelanggan

@bp.route('/pelanggan/<int:id>', methods=['GET'])
@login_required
def get_pelanggan(id):
    return jsonify(get_object_or_404(Pelanggan, Pelanggan.id==id).to_dict())

@bp.route('/pelanggan')
@login_required
def index_pelanggan():
    q = request.args.get('q', None)
    kota = request.args.get('kota', None)
    jatuh_tempo = request.args.get('jatuh_tempo', None)
    plafon = request.args.get('plafon', None)
    rst = Pelanggan.select()
    if q and len(q) > 3:
        rst = Pelanggan.select().where(Pelanggan.nama.contains(q))
    if kota and len(kota) > 3:
        rst = rst.where(Pelanggan.kota.contains(kota))
    if plafon and plafon.isdigit():
        rst = rst.where(Pelanggan.plafon > int(plafon) * 1000000)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Pelanggan.to_collection_dict(rst, page, per_page, 'api.index_pelanggan')
    return jsonify(data)