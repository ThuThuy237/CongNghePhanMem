import os
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from app import admin, app, utils, db
from flask import redirect, render_template, request
from flask_login import logout_user, current_user


class LogoutView(BaseView):
    @expose('/')
    def __index__(self):
        logout_user()
        return redirect('/')

    def is_accessible(self):
        return current_user.is_authenticated


class AddUserView(BaseView):
    @expose('/')
    def add(self):
        return self.render('admin/addUser.html')



class ManagerView(ModelView):
    """
    Nếu tài khoản đăng nhập có login_role == ADMIN thì hiển thị ManagerView
    """

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.login_role


admin.add_view(AddUserView(name='Add User'))
admin.add_view(LogoutView(name='Log Out'))
