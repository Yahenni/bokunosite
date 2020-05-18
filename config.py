import os

basedir = os.path.abspath(os.path.dirname(__name__))

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    CAPTCHA_IMAGE_PATH = os.path.join(basedir, 'app/base/static/captcha/')
    CAPTCHA_FONT_PATH = os.environ.get('CAPTCHA_FONT_PATH') or \
        os.path.join(basedir, 'app/base/static/fonts/Roboto-Regular.ttf')
    ARTICLES_PER_PAGE = os.environ.get('ARTICLES_ON_PAGE') or 15
    CODEMIRROR_LANGUAGES = ['markdown']
    CODEMIRROR_THEME = '3024-day'
    WTF_CSRF_ENABLED = True
    MARKDOWN_EXTRAS = ['break-on-newline', 'fenced-code-blocks']
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    if os.environ.get('ADMINS'):
        ADMINS = os.environ.get('ADMINS').split(';')
