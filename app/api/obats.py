from flask import jsonify, request
from playhouse.flask_utils import get_object_or_404
from app.api import bp
from app.models import Obat

@bp.route('/obat/<int:id>', methods=['GET'])
def get_obat(id):
    return jsonify(get_object_or_404(Obat, Obat.id==id).to_dict())

@bp.route('/obat')
def index_obat():
    rst = Obat.select()
    q = request.args.get('q', None)
    if q and len(q) > 3:
        rst = rst.where(Obat.nama.contains(q))
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Obat.to_collection_dict(rst, page, per_page, 'api.index_obat')
    return jsonify(data)