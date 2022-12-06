import datetime
from application import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


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


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.date.today())
    total = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='orders', uselist=False)
    meals = db.relationship('MealInOrder', back_populates='order')


class MealInOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'))
    meal = db.relationship('Meal', back_populates='orders')
    count = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    order = db.relationship('Order', back_populates='meals', uselist=False)
