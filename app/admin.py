import os
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from app import admin, app, utils
from flask import redirect, request
from flask_login import current_user


class AddUserView(BaseView):
    @expose('/', methods=['get', 'post'])
    def register(self):
        err_msg = ""
        if request.method == 'POST':
            password = request.form.get('password')
            confirm = request.form.get('confirm')
            if password == confirm:
                name = request.form.get('name')
                email = request.form.get('email')
                username = request.form.get('username')
                avatar = request.files["avatar"]

                avatar_path = 'images/upload/%s' % avatar.filename
                avatar.save(os.path.join(app.root_path,
                                         'static/',
                                         avatar_path))
                if utils.add_user(name=name, email=email, username=username,
                                  password=password, avatar=avatar_path):
                    return redirect('/')
                else:
                    err_msg = "Hệ thống đang có lỗi! Vui lòng quay lại sau!"
            else:
                err_msg = "Mật khẩu KHÔNG khớp!"

        return self.render('admin/addUser.html', err_msg=err_msg)

    def add(self):
        return self.render('admin/addUser.html')


class SellView(BaseView):
    @expose('/')
    def book_by_cate_list(self):
        books = utils.read_books()
        cate = utils.read_categories()
        return self.render('admin/sell.html', books=books, cate=cate)

    def add(self):
        return self.render('admin/sell.html')


class ManagerView(ModelView):
    """
    Nếu tài khoản đăng nhập có login_role == ADMIN thì hiển thị ManagerView
    """

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.login_role


admin.add_view(AddUserView(name='Add User'))
admin.add_view(SellView(name="Sell"))
# admin.add_view(LogoutView(name='Log Out'))
