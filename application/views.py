from flask import abort, flash, session, redirect, request, render_template, url_for
from flask_login import current_user, login_user, logout_user, login_required

from application import app, db, EXPIRE_LOGIN
from application.models import Category, Meal, User, Order, MealInOrder
from application.forms import OrderForm, LoginForm, RegisterForm


@app.route('/')
def main():
    categories = db.session.query(Category).all()
    return render_template('main.html', categories=categories)


@app.route('/account')
@login_required
def account():

    # orders = db.session.query(Order).
    return render_template('account.html')


@app.route('/auth')
def auth():
    return render_template('auth.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()
        login_user(user, remember=True, duration=EXPIRE_LOGIN)
        return redirect(url_for('account'))
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)  # type: ignore
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main'))


@app.route('/ordered')
def ordered():
    return render_template('ordered.html')


def in_cart(cart, id):
    """Returns index of item if in cart else False"""
    return next((int(index) for index, meal in enumerate(cart) if meal['id'] == id), False)


@app.route('/addtocart/<int:id>')
def add_to_cart(id):
    cart = session.get('cart', [])
    total = session.get('cart_total', 0)
    item = in_cart(cart, id)
    if item is not False:
        cart[item]['count'] += 1
        total += cart[item]['price']
    else:
        meal = db.session.query(Meal).get_or_404(id)
        cart.append({'id': id, 'price': meal.price, 'count': 1, 'title': meal.title})
        total += meal.price

    session['cart'] = cart
    session['cart_total'] = total
    return redirect(url_for('main'))


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    form = OrderForm()
    if form.validate_on_submit():
        order = Order(total=session['cart_total'], name=form.name.data, phone=form.tel.data,
                      address=form.address.data, user=current_user)
        db.session.add(order)
        for meal_data in session['cart']:
            meal = MealInOrder(meal_id=meal_data['id'], count=meal_data['count'], order=order)
            db.session.add(meal)
        db.session.commit()
        session.pop('cart')
        session.pop('cart_total')
        return redirect(url_for('ordered'))
    return render_template('cart.html', form=form)
