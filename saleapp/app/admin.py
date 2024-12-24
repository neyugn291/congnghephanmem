import hashlib

from app.models import Category, Book, User, UserRole, Regulation, Order, Receipt, ReceivedNote, OrderDetail
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, AdminIndexView
from flask_admin import Admin
from flask_login import current_user, logout_user
from flask import redirect
from app import app, db, dao

from sqlalchemy.exc import IntegrityError


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', stats=dao.books_stats(), UserRole=UserRole)

admin = Admin(app=app, name='Book Store Admin', template_mode='bootstrap4', index_view=MyAdminIndexView())

class CustomModelView(ModelView):
    extra_css = ['/static/css/custom_admin.css']


class AdminView(CustomModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class CategoryView(AdminView):
    column_list = ['name', 'books']
    page_size = 5


class BookView(AdminView):
    column_list = ['id', 'author', 'name', 'price']
    can_export = True
    column_searchable_list = ['name']
    page_size = 5
    column_filters = ['id', 'name', 'price']
    column_editable_list = ['name']

    def delete_model(self, model):
        replacement_book = Book.query.filter(Book.id == 0).first()

        for detail in model.received_note_details:
            detail.book_id = replacement_book.id

        for detail in model.order_details:
            detail.book_id = replacement_book.id

        for detail in model.receipts_details:
            detail.book_id = replacement_book.id

        for comment in model.comments:
            comment.book_id = replacement_book.id

        db.session.commit()
        super().delete_model(model)


class UserView(AdminView):
    column_list = ['id', 'username', 'password', 'user_role']
    page_size = 5
    form_columns = ['name', 'username', 'password', 'email', 'phone', 'location', 'user_role']

    def on_model_change(self, form, model, is_created):
        if 'password' in form:
            model.password = str(hashlib.md5(model.password.encode('utf-8')).hexdigest())

    def delete_model(self, model):
        replacement_user = User.query.filter(User.id == 0).first()

        for order in model.orders:
            order.user_id = replacement_user.id

        for comment in model.comments:
            comment.user_id = replacement_user.id

        db.session.commit()
        super().delete_model(model)



class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

class RegulationView(AdminView):
    can_create = False
    can_delete = False
    can_edit = True



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
admin.add_view(RegulationView(Regulation, db.session))
admin.add_view(StatsView(name='Thống kê'))
admin.add_view(LogoutView(name='Đăng xuất'))
