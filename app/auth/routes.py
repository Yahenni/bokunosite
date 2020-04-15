from flask import render_template, flash, redirect, url_for
from flask_login import current_user, logout_user, login_user, login_required

from app.auth import auth
from app.models import User
from .forms import LoginForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильный пароль или имя пользователя', 'error')
            return redirect(url_for('.login'))
        login_user(user, remember=form.remember_me.data)
        flash('Успешно вошли')
        return redirect(url_for('index'))
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
    return redirect(url_for('index'))
