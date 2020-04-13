from flask import jsonify, g
from flask_login import current_user, login_required

from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth


@bp.route('/token/', methods=['GET'])
@login_required
def get_token():
    if not current_user.is_authenticated:
        return jsonify({"error": "Unauthorized"})
    token = current_user.get_token()
    db.session.commit()
    return jsonify({"token": token})


@bp.route('/token/', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    g.current_user.revoke_token()
    db.session.commit()
    return '', 204
