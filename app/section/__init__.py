from flask import Blueprint

section = Blueprint(
    'section',
    __name__,
    url_prefix='/section/',
    template_folder='templates',
    static_folder='static'
)

from app.section import routes, forms
