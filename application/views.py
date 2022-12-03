from flask import abort, flash, session, redirect, request, render_template, session, url_for
from application import app, db
from application.models import Category, Meal
from application.forms import OrderForm


@app.route('/')
def main():
    categories = db.session.query(Category).all()
    return render_template('main.html', categories=categories)


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    form = OrderForm()

    if form.validate_on_submit():
        return redirect(url_for('ordered'))
    return render_template('cart.html', form=form)


@app.route('/account')
def account():
    return render_template('account.html')


@app.route('/auth')
def auth():
    return render_template('auth.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/logout')
def logout():
    pass


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
