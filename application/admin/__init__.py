from flask import abort
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from wtforms import PasswordField
from wtforms.validators import EqualTo

from application import db, app
from application.models import User, Order, Meal, MealInOrder, Category


# Create customized model view class with check admin role
class MyModelView(ModelView):
    create_modal = True
    edit_modal = True

    def is_accessible(self):
        return current_user.is_anonymous is False and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        abort(403, description='Доступно только админам')


class UserView(MyModelView):
    column_searchable_list = ['email', 'is_admin']
    column_filters = ['is_admin']
    column_editable_list = ['is_admin']
    column_exclude_list = ['password_hash']
    form_excluded_columns = ['password_hash', 'orders']
    form_extra_fields = {
        'set_password': PasswordField('New password'),
        'confirm_password': PasswordField('Confirm new password',
                                          validators=[EqualTo('set_password', message='Пароли на совпадают')])
    }
    form_widget_args = {
        'set_password': {
            'autocomplete': 'new-password'
        },
        'confirm_password': {
            'autocomplete': 'new-password'
        }
    }

    def on_model_change(self, form, User, is_created):
        if 'set_password' in form.data:
            if form.set_password.data:
                User.password = form.set_password.data
            else:
                del form.set_password


class OrderView(MyModelView):
    column_searchable_list = ['name', 'status']
    column_filters = ['status', 'user_id']
    column_editable_list = ['status']
    form_excluded_columns = ['date']
    form_choices = {
        'status': [
            ('В обработке', 'В обработке'),
            ('Готовится', 'Готовится'),
            ('Передан на доставку', 'Передан на доставку'),
            ('Доставлен', 'Доставлен'),
            ('Отменён', 'Отменён')
        ]
    }


class MealView(MyModelView):
    # column_exclude_list = ['password_hash']
    form_excluded_columns = ['orders']


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_anonymous is False and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        abort(403, description='Доступно только админам')


# Create admin
admin = Admin(app, name='CRM', template_mode='bootstrap4', index_view=MyAdminIndexView(url='/crm'))

# Add views
admin.add_view(UserView(User, db.session))
admin.add_view(OrderView(Order, db.session))
admin.add_view(MealView(Meal, db.session))
admin.add_view(MyModelView(MealInOrder, db.session))
admin.add_view(MyModelView(Category, db.session))
