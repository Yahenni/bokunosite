from threading import Thread

from flask import render_template
from flask_mail import Message

from app import mail, config, app


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def send_email_confirmation(user):
    token = user.get_email_confirmation_token()
    send_email('[Boku no site] Подвердите вашу почту.',
               sender=config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/confirm_email.txt',
                                         user=user, token=token),
               html_body=render_template('email/confirm_email.html',
                                         user=user, token=token))


def send_password_reset(user):
    token = user.get_reset_password_token()
    send_email('[Boku no site] Подвердите смену пароля.',
               sender=config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/confirm_password_reset.txt',
                                         user=user, token=token),
               html_body=render_template('email/confirm_password_reset.html',
                                         user=user, token=token))
