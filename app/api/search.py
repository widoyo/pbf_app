from flask import jsonify, request
from playhouse.flask_utils import get_object_or_404
from flask_login import login_required, current_user
from app.api import bp
from app.models import Pelanggan


@bp.route('/search/pelanggan')
def search_pelanggan():
    q = request.args.get('q', None)
    if q and len(q) > 2:
        rst = Pelanggan.select().where(Pelanggan.nama % '*' + q + '*')
        return jsonify({'items': [r.to_dict() for r in rst]})
    return jsonify({'items': []})