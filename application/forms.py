from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TelField
from wtforms.validators import DataRequired, Length


class OrderForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired(message='Незнакомым не доставляем')])
    address = StringField('Адрес', validators=[DataRequired(message='Мы не знаем где твой дом'),
                                               Length(min=5, message='Это не похоже на адрес')])
    tel = TelField('Телефон', validators=[DataRequired(message='Как курьер позвонит?'),
                                          Length(min=3, message='Таких номеров не бывает')])
    submit = SubmitField('Оформить заказ')
