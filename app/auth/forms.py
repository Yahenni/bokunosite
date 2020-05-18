from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, \
                    HiddenField, SubmitField,   \
                    BooleanField
from wtforms.validators import InputRequired, Email, \
                               DataRequired, ValidationError, \
                               EqualTo

from app.models import User


class LoginForm(FlaskForm):
    username = StringField(
        'Имя пользователя: ',
        validators=[InputRequired()],
        render_kw={
            "placeholder": "Username",
            "class": "form-control",
            "type": "username"
        }
    )
    password = PasswordField(
        'Пароль:',
        validators=[InputRequired()],
        render_kw={
            "placeholder": "Password",
            "class": "form-control"
        }
    )
    hash = HiddenField(label=None)
    submit = SubmitField(
        "Войти",
        render_kw={"class": "btn btn-lg btn-primary btn-block"}
    )
    remember_me = BooleanField("Запомнить меня")


class ResetPasswordForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email()])
    hash = HiddenField()
    submit = SubmitField('Выслать письмо',)

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Почта не найдена')


class SignupForm(FlaskForm):
    username = StringField(
        'Имя пользователя: ',
        validators=[InputRequired()],
    )
    email = StringField('Email', validators=[DataRequired(), Email()])
    hash = HiddenField()
    submit = SubmitField("Зарегестрироваться")
    password = PasswordField(
        'Пароль:',
        validators=[
            DataRequired(),
            EqualTo('confirm', message='Пароли должны совпадать')
        ]
    )
    confirm = PasswordField(
        'Повторите пароль: ',
        validators=[DataRequired()]
    )

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, используйте другое имя'
                                  ' пользователя')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, используйте другой'
                                  ' адресс эл. почты')


class ChangePasswordForm(FlaskForm):
    password = PasswordField(
        'Пароль:',
        validators=[DataRequired()]
    )
    confirm = PasswordField(
        'Повторите пароль',
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField("Сменить пароль")
