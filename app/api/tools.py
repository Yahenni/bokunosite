from flask import jsonify, request
from markdown2 import markdown

from app import config
from app.api import bp
from app.api.errors import bad_request


@bp.route('/markdown', methods=['POST'])
def markdown_render():
    data = request.get_json()['data']
    if len(data) > 50000:
        return bad_request()
    else:
        return jsonify({
            "html": markdown(data, extras=config['MARKDOWN_EXTRAS'])
        })
