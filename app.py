
from application import app
from application.models import User, Order, Meal, MealInOrder, Category


# @app.shell_context_processor
# def make_shell_context():
#     return {'db': db, 'User': User, 'Order': Order, 'Meal': Meal, 'Category': Category, 'MealInOrder': MealInOrder}


# app.run()
if __name__ == '__main__':
    app.run()
