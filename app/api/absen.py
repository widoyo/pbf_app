import datetime
import json
from flask import jsonify, request
from playhouse.flask_utils import get_object_or_404
from flask_login import login_required, current_user
from app.api import bp
from app.models import Absen

@bp.route('/absen/today', methods=['PUT'])
@login_required
def absen_close():
    ret = {'ok': False}
    data = request.get_json() or {}
    present = Absen.get(data.get('id'))
    present.keluar = datetime.datetime.now()
    present.save()
    return jsonify(present.to_dict())

@bp.route('/absen/today', methods=['GET'])
#@login_required
def absen_today():
    d = datetime.date.today()
    rst = Absen.select().where((Absen.username==current_user.username) & (Absen.tanggal==d)).limit(1).order_by(Absen.tanggal.desc())
    ret = {}
    if rst.count() > 0:
        ret = rst[0].to_dict()
    return jsonify(ret)

@bp.route('/absen/today', methods=['POST'])
#@login_required
def masuk_today():
    data = request.get_json() or {}
    for f in ('ll', 'keterangan'):
        if f not in data:
            ret = {'ok': False, 'msg': '{} tidak boleh kosong'.format(f)}
            return jsonify(ret)
    new_absen = Absen()
    data.update({'username': current_user.username})
    new_absen.from_dict(data)
    return new_absen.to_dict()

@bp.route('/absen')
@login_required
def absen():
    d = datetime.date.today()
    if current_user.role == 0:
        data = [r.to_dict() for r in Absen.select().where(Absen.keluar==None)]
    else:
        data = [r.to_dict() for r in Absen.select().where(Absen.tanggal.month()==d.month)]
    return jsonify(data)
