from flask_wtf import FlaskForm
from flask_codemirror.fields import CodeMirrorField
from wtforms import StringField, SelectField,     \
                    PasswordField, TextAreaField, \
                    SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, \
                               InputRequired, EqualTo


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
    data = CodeMirrorField(language='markdown', config={'lineNumbers': 'true'})
    hash = HiddenField(label=None)
    submit = SubmitField("Отправить")
