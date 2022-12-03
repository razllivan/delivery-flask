from application import app, db
from application.models import Meal, Category
import csv


def add_meals(meals):
    with app.app_context():
        for meal_data in meals:
            meal = Meal(
                title=meal_data['title'],
                price=meal_data['price'],
                description=meal_data['description'],
                picture=meal_data['picture'],
                category_id=meal_data['category_id'],
            )
            db.session.add(meal)
        db.session.commit()


def add_categories(categories):
    with app.app_context():
        for category_data in categories:
            category = Category(
                title=category_data['title']
            )
            db.session.add(category)
        db.session.commit()


def main():
    with open('delivery_categories.csv', encoding='utf-8') as f:
        categories = csv.DictReader(f, delimiter=',')
        add_categories(categories)

    with open('delivery_items.csv', encoding='utf-8') as f:
        meals = csv.DictReader(f, delimiter=',')
        add_meals(meals)


if __name__ == '__main__':
    main()
