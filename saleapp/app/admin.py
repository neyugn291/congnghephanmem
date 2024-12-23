import hashlib

from app.models import Category, Book, User, UserRole
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, AdminIndexView
from flask_admin import Admin
from flask_login import current_user, logout_user
from flask import redirect
from app import app, db, dao

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', stats=dao.books_stats(), UserRole=UserRole)

admin = Admin(app=app, name='Book Store Admin', template_mode='bootstrap4', index_view=MyAdminIndexView())

class CustomModelView(ModelView):
    extra_css = ['/static/css/custom_admin.css']
    extra_js = ['/custom.js']

class AdminView(CustomModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class CategoryView(AdminView):
    column_list = ['name', 'books']
    page_size = 5


class BookView(AdminView):
    column_list = ['id','author' , 'name', 'price']
    can_export = True
    column_searchable_list = ['name']
    page_size = 5
    column_filters = ['id', 'name', 'price']
    column_editable_list = ['name']

class UserView(AdminView):
    column_list = ['id', 'username', 'password', 'user_role']
    page_size = 5
    form_columns = ['name','username', 'password','email','phone', 'location', 'user_role']

    def on_model_change(self, form, model, is_created):
        if 'password' in form:
            model.password = str(hashlib.md5(model.password.encode('utf-8')).hexdigest())

class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/login')


class StatsView(AuthenticatedView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html', stats=dao.revenue_stats(), stats2=dao.revenue_time())


admin.add_view(CategoryView(Category, db.session))
admin.add_view(BookView(Book, db.session))
admin.add_view(UserView(User, db.session))
admin.add_view(StatsView(name='Thống kê'))
admin.add_view(LogoutView(name='Đăng xuất'))
