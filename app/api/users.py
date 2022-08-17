from flask import jsonify
from playhouse.flask_utils import get_object_or_404
from app.api import bp
from app.models import User

@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    return jsonify(get_object_or_404(User, User.id==id).to_dict())
