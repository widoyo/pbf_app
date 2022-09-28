'''API Penjualan'''
from flask import jsonify, request, url_for
from playhouse.flask_utils import get_object_or_404

from app.api import bp
from app.models import Jual, ItemJual


@bp.route('/penjualan/<int:id>/item', methods=['POST'])
def add_item_penjualan():
    data = request.get_json() or {}
    itemjual = ItemJual()
    
@bp.route('/penjualan/<int:id>', methods=['GET'])
def get_penjualan(id):
    return jsonify(get_object_or_404(Jual, Obat.id==id).to_dict())

@bp.route('/penjualan', methods=['POST'])
def create_pesanan():
    data = request.get_json() or {}
    penjualan = Jual()
    penjualan.from_dict(data)
    penjualan.save()
    response = jsonify(penjualan.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_penjualan', id=penjualan.id)
    return response

@bp.route('/penjualan')
def index_jual():
    juals = [j.to_dict() for j in Jual.select()]
    return jsonify(juals)