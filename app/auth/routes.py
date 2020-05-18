from flask import render_template, flash, redirect, url_for
from flask_login import current_user, logout_user, login_user, login_required

from app import db
from app.auth import auth
from app.models import User, CaptchaStore
from .forms import LoginForm, ResetPasswordForm, SignupForm, ChangePasswordForm
from app.email import send_email_confirmation, send_password_reset


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Вы уже вошли')
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильный пароль или имя пользователя', 'error')
            return redirect(url_for('.login'))
        login_user(user, remember=form.remember_me.data)
        flash('Успешно вошли')
        return redirect(url_for('base.index'))
    return render_template(
        'login.html',
        title='Login',
        navbar_off=True,
        message_off=True,
        form=form
    )


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('base.index'))


@auth.route('/reset', methods=['GET', 'POST'])
def reset():
    form = ResetPasswordForm()
    if current_user.is_authenticated:
        return redirect(url_for('base.index'))
    if form.validate_on_submit():
        captcha = CaptchaStore.query.filter_by(
            hash=form.hash.data).first()
        if captcha is None:
            flash(
                'Каптча неверна. Пожалуйста, решите ее перед регистрацией'
            )
            return redirect(url_for('.reset'))
        captcha.remove_picture()
        db.session.delete(captcha)
        db.session.commit()
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset(user)
        flash('Письмо отправленно. Проверьте вашу почту')
        return redirect(url_for('base.index'))

    return render_template(
        'reset_password_request.html',
        title="Сбросить пароль",
        navbar_off=True,
        message_off=True,
        form=form
    )


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('base.index'))
    form = SignupForm()
    if form.validate_on_submit():
        captcha = CaptchaStore.query.filter_by(
            hash=form.hash.data).first()
        if captcha is None:
            flash(
                'Каптча неверна. Пожалуйста, решите ее перед регистрацией'
            )
            return redirect(url_for('.signup'))
        captcha.remove_picture()
        db.session.delete(captcha)
        db.session.commit()
        user = User(
            username=form.username.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        send_email_confirmation(user)
        flash("Пожалуйста, подвердите вашу почту."
              " Письмо уже выслано")
        return redirect(url_for('base.index'))
    return render_template(
        'signup.html',
        title="Зарегестрироваться",
        navbar_off=True,
        message_off=True,
        form=form,
    )


@auth.route('/confirm_email/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    if current_user.is_authenticated:
        return redirect(url_for('base.index'))
    user = User.verify_email_confirmation_token(token)
    if not user:
        flash("Ошибка")
        return redirect(url_for('base.index'))
    user.email_verifed = True
    db.session.commit()
    flash('Вы успешно подвердили эл. почту!')
    return redirect(url_for('.login'))


@auth.route('/change_password/<token>', methods=['GET', 'POST'])
def change_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        flash("Ошибка")
        return redirect(url_for('base.index'))
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Вы успешно изменили пароль!")
        return redirect(url_for('login'))
    return render_template(
        'change_password.html',
        title='Измените пароль',
        navbar_off=True,
        message_off=True,
        form=form,
    )
