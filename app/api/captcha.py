from flask import make_response, redirect, url_for, jsonify

from app.api import api
from app import db
from app.models import CaptchaStore
from app.api.errors import not_found


@api.route('/captcha/')
def get_captcha():
    captcha = CaptchaStore()
    captcha.create_picture()
    db.session.add(captcha)
    db.session.commit()

    response = {
        'key': captcha.hash,
        'image_url': captcha.image,
    }
    return jsonify(response)


@api.route('/captcha/<hash>')
def refresh_captcha(hash):
    captcha = CaptchaStore.query.filter_by(hash=hash).first()
    if captcha is None:
        return not_found("captcha not found")
    captcha.remove()
    db.session.commit()
    return redirect(url_for('api.get_captcha'))


@api.route('/captcha/<hash>/<text>')
def validate_captcha(hash, text):
    captcha = CaptchaStore.query.filter_by(hash=hash).first()
    if captcha is None:
        return not_found("captcha not found")
    captcha.decided = True
    db.session.commit()
    if captcha.value == text:
        return make_response("", 200)
    else:
        return make_response("", 400)
