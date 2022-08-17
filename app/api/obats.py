from flask import jsonify
from playhouse.flask_utils import get_object_or_404
from app.api import bp
from app.models import Obat

@bp.route('/obat/<int:id>', methods=['GET'])
def get_obat(id):
    return jsonify(get_object_or_404(Obat, Obat.id==id).to_dict())

@bp.route('/obat')
def index_obat():
    return jsonify()