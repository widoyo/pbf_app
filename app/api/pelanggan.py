from flask import jsonify, request
from playhouse.flask_utils import get_object_or_404
from app.api import bp
from app.models import Pelanggan

@bp.route('/pelanggan/<int:id>', methods=['GET'])
def get_pelanggan(id):
    return jsonify(get_object_or_404(Pelanggan, Pelanggan.id==id).to_dict())

@bp.route('/pelanggan')
def index_pelanggan():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Pelanggan.to_collection_dict(Pelanggan.select(), page, per_page, 'api.index_pelanggan')
    return jsonify(data)