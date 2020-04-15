from flask import render_template, url_for
from flask_login import current_user, login_required

from app.base import base
from app.models import Section


@base.route('/')
@base.route('/index')
def index():
    print(url_for('.static', filename="kot.png"))
    return render_template(
        "index.html",
        title="Index Page",
        sections=Section.query.all(),
    )
