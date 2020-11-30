import os
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView

from app import admin, app, utils, db
from flask import redirect, render_template, request
from flask_login import logout_user, current_user
from app.models import Login


class LogoutView(BaseView):
    @expose('/')
    def __index__(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


# class AddUserView(BaseView):
#     @expose('/')
#     def __index__(self):
#         err_msg = ""
#         if request.method == 'POST':
#             password = request.form.get('password')
#             confirm = request.form.get('confirm')
#             if password == confirm:
#                 name = request.form.get('name')
#                 email = request.form.get('email')
#                 username = request.form.get('username')
#                 avatar = request.files["avatar"]
#
#                 avatar_path = 'images/upload/%s' % avatar.filename
#                 avatar.save(os.path.join(app.root_path,
#                                          'static/',
#                                          avatar_path))
#                 if utils.add_user(name=name, email=email, username=username,
#                                   password=password, avatar=avatar_path):
#                     return redirect('/')
#                 else:
#                     err_msg = "Hệ thống đang có lỗi! Vui lòng quay lại sau!"
#             else:
#                 err_msg = "Mật khẩu KHÔNG khớp!"
#
#         return render_template('/admin/addUser.html', err_msg=err_msg)
#
#     def is_accessible(self):
#         return current_user.is_authenticated
# class StaffView(ModelView):
#     def is_accessible(self):
#         return current_user.is_authenticated
#
#
class ManagerView(ModelView):
    """
    Nếu tài khoản đăng nhập có login_role == ADMIN thì hiển thị ManagerView
    """
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.login_role
#
#
# admin.add_view(StaffView(Customer, db.session))
# admin.add_view(StaffView(Employee, db.session))
# admin.add_view(StaffView(Categories, db.session))
# admin.add_view(StaffView(Publisher, db.session))
# admin.add_view(StaffView(Order, db.session))
# admin.add_view(StaffView(Supplier, db.session))
# admin.add_view(StaffView(Books, db.session))
admin.add_view(ManagerView(Login, db.session, name="Manager"))


# admin.add_view(AddUserView(name='Add User'))
admin.add_view(LogoutView(name='Log Out'))
