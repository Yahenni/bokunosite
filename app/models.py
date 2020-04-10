from datetime import datetime

from app import db


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shortname = db.Column(db.String(64), index=True, unique=True)
    longname = db.Column(db.String(128), unique=True)
    aritcles = db.relationship('Article', backref='owner', lazy='dynamic')

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

    def __repr__(self):
        return 'Article <{}>'.format(self.id)
