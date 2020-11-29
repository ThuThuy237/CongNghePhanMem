from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from app import admin
from flask import redirect, session
from app.models import *
from flask_login import logout_user, current_user


class LogoutView(BaseView):
    @expose('/')
    def __index__(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class StaffView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class ManagerView(ModelView):
    """
    Nếu tài khoản đăng nhập có access == True thì hiển thị ManagerView
    """
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.access


admin.add_view(StaffView(Customer, db.session))
admin.add_view(StaffView(Employee, db.session))
admin.add_view(StaffView(Categories, db.session))
admin.add_view(StaffView(Publisher, db.session))
admin.add_view(StaffView(Order, db.session))
admin.add_view(StaffView(Supplier, db.session))
admin.add_view(StaffView(Books, db.session))
admin.add_view(ManagerView(Login, db.session, name="Manager"))
admin.add_view(LogoutView(name='Log Out'))
