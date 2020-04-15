from flask import jsonify, make_response, url_for, g

from app import db
from app.models import Article
from app.api import api
from app.api.auth import token_auth
from app.api.errors import not_found, forbidden


@api.route('/article/<int:id>/remove/', methods=['POST'])
@token_auth.login_required
def remove_article(id):
    article = Article.query.filter_by(id=id).first()
    if article is None:
        return not_found("article not found")
    if not g.current_user.privilege > 0:
        return forbidden("Forbidden")
    article.remove()
    db.session.commit()
    return make_response("", 200)
