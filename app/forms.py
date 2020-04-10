from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, \
                    BooleanField, SubmitField, \
                    SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, InputRequired

from app import db
from app.models import Section


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
    title = StringField('Название: ', validators=[DataRequired()])
    data = TextAreaField('Текст: ', validators=[Length(min=0, max=3000)])
    submit = SubmitField("Отправить")
