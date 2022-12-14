from application import db, app
from flask import abort
from application.models import User, Order, Meal, MealInOrder
from flask_login import current_user
from flask_admin import Admin, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView


# Create customized model view class with check admin role
class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_anonymous is False and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        abort(403, description='Доступно только админам')


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_anonymous is False and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        abort(403, description='Доступно только админам')


# Create admin
admin = Admin(app, name='CRM', template_mode='bootstrap4', index_view=MyAdminIndexView(url='/crm'))

# Add views
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Order, db.session))
admin.add_view(MyModelView(Meal, db.session))
admin.add_view(MyModelView(MealInOrder, db.session))
