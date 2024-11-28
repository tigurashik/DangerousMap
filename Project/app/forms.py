from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Regexp
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=64)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Это имя пользователя уже занято.')

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class PointForm(FlaskForm):
    coordinates = StringField('Долгота и Широта (через запятую)', validators=[
        DataRequired(),
        Regexp(r'^-?\d+(\.\d+)?\s*,\s*-?\d+(\.\d+)?$', message="Введите координаты в формате 'долгота, широта'"),
    ])
    description = TextAreaField('Описание', validators=[Length(max=500)])
    submit = SubmitField('Добавить точку')
