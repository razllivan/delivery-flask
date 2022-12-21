from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TelField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from application.models import db, User


class OrderForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired(message='Незнакомым не доставляем')])
    address = StringField('Адрес', validators=[DataRequired(message='Мы не знаем где твой дом'),
                                               Length(min=5, message='Это не похоже на адрес')])
    tel = TelField('Телефон', validators=[DataRequired(message='Как курьер позвонит?'),
                                          Length(min=3, message='Таких номеров не бывает')])
    submit = SubmitField('Оформить заказ')


class LoginForm(FlaskForm):
    email = EmailField('Электронная почта', validators=[DataRequired(message='Надо указать почту'),
                                                        Email(message='Кажется это не эл.почта')])
    password = PasswordField('Пароль', validators=[DataRequired(message='Пароль не может быть пустым')])
    submit = SubmitField('Войти')

    def validate_email(self, email):
        user = db.session.query(User).filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Пользователь с такой почтой не зарегистрирован')

    def validate_password(self, password):
        if user := db.session.query(User).filter_by(email=self.email.data).first():
            if user.is_valid_password(password.data) is False:
                raise ValidationError('Пароль неверный')


class RegisterForm(FlaskForm):
    email = EmailField('Электронная почта', validators=[DataRequired(message='Надо указать почту'),
                                                        Email(message='Кажется это не эл.почта')])
    password = PasswordField('Пароль', validators=[DataRequired(message='Пароль не может быть пустым'),
                                                   Length(min=6, message='Длина пароля должна быть больше 5')])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(message='Надо повторить пароль'),
                                                              EqualTo('password', message='Пароль не совпадает')])
    submit = SubmitField('Зарегистрироваться')

    def validate_email(self, email):
        user = db.session.query(User).filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Пользователь с такой почтой уже зарегистрирован')
