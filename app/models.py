from datetime import datetime
from random import choice
import os

from werkzeug.security import generate_password_hash, check_password_hash
from markdown import markdown
from captcha.image import ImageCaptcha
from flask import url_for
from flask_login import UserMixin

from app import db, config, login


image = ImageCaptcha(fonts=[config["CAPTCHA_FONT_PATH"]])


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shortname = db.Column(db.String(64), index=True, unique=True)
    longname = db.Column(db.String(128), unique=True)
    articles = db.relationship('Article', backref='owner', lazy='dynamic')

    def __repr__(self):
        return 'Section <{}>'.format(self.shortname)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    html_body = db.Column(db.Text)
    markdown_body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    tripcode = db.Column(db.String(128), index=True)
    title = db.Column(db.String(128))
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))
    poster_name = db.Column(db.String(64))
    formated_timestamp = db.Column(db.String(128))
    description = db.Column(db.String())

    def create_tripcode(self, password):
        self.tripcode = generate_password_hash(password)[-12:]

    def create_html(self):
        self.html_body = markdown(self.markdown_body)

    def format_timestamp(self):
        self.formated_timestamp = self.timestamp.strftime('%Y-%m-%d %H:%M')

    def __repr__(self):
        return 'Article <{}>'.format(self.id)


class CaptchaStore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String(128))
    value = db.Column(db.String(64))
    decided = db.Column(db.Boolean, default=False)
    image = db.Column(db.String(128))

    def remove_picture(self):
        os.remove("{}{}.png".format(
            config["CAPTCHA_IMAGE_PATH"],
            self.hash
        ))

    def create_picture(self):
        string = \
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        self.value = ''.join(choice(string) for i in range(6))
        self.hash = generate_password_hash(self.value)[-12:]
        image.write(
            self.value,
            "{}{}.png".format(
                config['CAPTCHA_IMAGE_PATH'],
                self.hash
            )
        )
        self.image = url_for(
            'static',
            filename='captcha/{}.png'.format(self.hash)
        )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    privilege = db.Column(db.Integer, default=0)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
