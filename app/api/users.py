from flask import jsonify
from playhouse.flask_utils import get_object_or_404
from flask_login import current_user, login_required
from app.api import bp
from app.models import User

@bp.route('/user/<int:id>', methods=['GET'])
@login_required
def get_user(id):
    return jsonify(get_object_or_404(User, User.id==id).to_dict())

@bp.route('/user/<username>', methods=['POST'])
@login_required
def user_set_password(username, password):
    user = User.get(User.username==username)
    user.set_password(password)
    user.save()
    return jsonify(user)