from flask import jsonify

from app.models import db
from app.api import bp
from app.api.auth import basic_auth

@bp.route('/token', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    return jsonify({'token': token})
    pass

def revoke_token():
    pass
