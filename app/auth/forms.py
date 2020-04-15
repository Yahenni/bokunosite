from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, \
                    HiddenField, SubmitField,   \
                    BooleanField
from wtforms.validators import InputRequired


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
