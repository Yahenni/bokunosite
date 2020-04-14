from flask_wtf import FlaskForm
from flask_codemirror.fields import CodeMirrorField
from wtforms import StringField, PasswordField, \
                    BooleanField, SubmitField, \
                    SelectField, TextAreaField, \
                    HiddenField
from wtforms.validators import DataRequired, Length, EqualTo, InputRequired


class ArticlePostForm(FlaskForm):
    username = StringField('Имя: ', default="Анонимус")
    section = SelectField('Раздел: ', coerce=int)
    password = PasswordField(
        'Пароль: ',
        validators=[
            InputRequired(),
            EqualTo('confirm', message='Пароли должны совпадать')
        ]
    )
    confirm = PasswordField('Повторите пароль: ')
    title = StringField(
        'Название: ',
        validators=[DataRequired(), Length(min=3, max=80)])
    description = TextAreaField(
        'Описание (опционально): ',
        validators=[Length(min=0, max=300)],
        render_kw={
            "minlength": "0",
            "maxlength": "300",
        }
    )
    """
    data = TextAreaField(
        'Текст: ',
        validators=[DataRequired(), Length(min=0, max=50000)],
        render_kw={
            "minlength": "0",
            "maxlength": "3000",
            "rows": "8"
        },
        id="editor"
    )
    """
    data = CodeMirrorField(language='markdown', config={'lineNumbers': 'true'})
    hash = HiddenField(label=None)
    submit = SubmitField("Отправить")


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
