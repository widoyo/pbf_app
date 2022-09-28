'''
aktifitas.py

model: Moving
'''
import datetime
import json
from flask import jsonify, request
from playhouse.flask_utils import get_object_or_404
from flask_login import login_required, current_user
from app.api import bp
from app.models import Moving

@bp.route('/aktifitas', methods=['POST'])
@login_required
def aktifitas_today():
    data = request.get_json() or {}
    if data == {}:
        return jsonify({'ok': False})
    data.update({'username': current_user.username})
    new_move = Moving()
    nm = new_move.from_dict(data)
    return jsonify(nm.to_dict())