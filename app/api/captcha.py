import json

from flask import make_response, redirect, url_for

from app.api import bp
from app import db
from app.models import CaptchaStore


@bp.route('/captcha/')
def get_captcha():
    captcha = CaptchaStore()
    captcha.create_picture()
    db.session.add(captcha)
    db.session.commit()
    print(captcha.image)

    to_json_response = {
        'key': captcha.hash,
        'image_url': captcha.image,
    }

    resp = make_response(json.dumps(to_json_response))
    resp.content_type = 'application/json'
    return resp


@bp.route('/captcha/<hash>')
def refresh_captcha(hash):
    captcha = CaptchaStore.query.filter_by(hash=hash).first_or_404()
    db.session.delete(captcha)
    db.session.commit()
    return redirect(url_for('api.get_captcha'))


@bp.route('/captcha/<hash>/<text>')
def validate_captcha(hash, text):
    captcha = CaptchaStore.query.filter_by(hash=hash).first_or_404()
    captcha.decided = True
    db.session.commit()
    if captcha.value == text:
        return make_response("", 200)
    else:
        return make_response("", 400)
