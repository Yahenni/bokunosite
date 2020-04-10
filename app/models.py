from datetime import datetime

from werkzeug.security import generate_password_hash
from markdown import markdown

from app import db


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

    def create_tripcode(self, password):
        self.tripcode = generate_password_hash(password)[-12:]

    def create_html(self):
        self.html_body = markdown(self.markdown_body)

    def __repr__(self):
        return 'Article <{}>'.format(self.id)
