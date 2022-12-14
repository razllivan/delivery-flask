import datetime

from flask import abort
from flask_admin import AdminIndexView


from application import db, login_manager, admin
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin.contrib.sqla import ModelView


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String, nullable=False)
    orders = db.relationship('Order', back_populates='user')

    @property
    def password(self):
        raise AttributeError('Вам не нужно знать пароль')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def is_valid_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))


class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    picture = db.Column(db.String, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='meals', uselist=False)
    orders = db.relationship('MealInOrder', back_populates='meal')


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    meals = db.relationship('Meal', back_populates='category')

    def __repr__(self):
        return f'<{self.title}>'


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, default=datetime.date.today())
    total = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, default='В обработке')
    phone = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='orders', uselist=False)
    meals = db.relationship('MealInOrder', back_populates='order', cascade='all, delete, delete-orphan')

    def __repr__(self):
        return f'<Order {self.id} from user {self.user_id}>'


class MealInOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'))
    meal = db.relationship('Meal', back_populates='orders')
    count = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    order = db.relationship('Order', back_populates='meals', uselist=False)

    def __repr__(self):
        return f'<Meal {self.meal_id} in order {self.order_id}>'



