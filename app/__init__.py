from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_codemirror import CodeMirror
from flask_mail import Mail

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
config = app.config
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

bootstrap = Bootstrap(app)
codemirror = CodeMirror(app)
mail = Mail(app)

from app.base import base
from app.api import api
from app.section import section
from app.auth import auth

BLUEPRINTS = (base, api, section, auth)

for blueprint in BLUEPRINTS:
    app.register_blueprint(blueprint)
