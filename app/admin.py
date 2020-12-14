import os
from flask_admin import BaseView, expose
from flask_admin.model.template import macro
from flask_admin.contrib.sqla import ModelView
from app import admin, app, utils, db
from flask import redirect, request
from flask_login import current_user, logout_user

from app.models import Employee, Login, Supplier, Publisher, Categories, LoginRole, Books, Regulations


# class AddUserView(BaseView):
#     @expose('/', methods=['get', 'post'])
#     def register(self):
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
#                                   password=password, avatar='/static/'+avatar_path):
#                     return redirect('/admin/adduserview/')
#                 else:
#                     err_msg = "Hệ thống đang có lỗi! Vui lòng quay lại sau!"
#             else:
#                 err_msg = "Mật khẩu KHÔNG khớp!"
#
#         return self.render('admin/addUser.html', err_msg=err_msg)
#
#     def add(self):
#         return self.render('admin/addUser.html')


class SellView(BaseView):
    @expose('/', methods=['get', 'post'])
    def book_by_cate_list(self):
        list_book = utils.read_books()
        cate = utils.read_categories()
        customer = utils.read_customers()
        return self.render('admin/sell.html', list_book=list_book, cate=cate, customer=customer)


class ImportView(BaseView):
    @expose('/', methods=['get', 'post'])
    def imp(self):
        list_book = utils.read_books()
        cate = utils.read_categories()
        supplier = utils.read_supplier()
        return self.render('admin/import.html', list_book=list_book, cate=cate, supplier=supplier)

    def add(self):
        return self.render('admin/import.html')


class ManagerView(ModelView):
    """
    Nếu tài khoản đăng nhập có login_role == ADMIN thì hiển thị ManagerView
    """

    def is_accessible(self):
        if current_user.is_authenticated:
            if(current_user.login_role == LoginRole.ADMIN):
                return current_user.login_role


class ChangeRegulateView(ManagerView):
    can_create = False
    can_delete = False
    can_edit = False
    column_editable_list = ['inventory_min_when_import', 'inventory_min_when_sell', 'import_min', 'debt_max', 'active']
    column_exclude_list = ('login')


class LogoutView(BaseView):
    @expose('/')
    def __index__(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated

admin.add_view(SellView(name="Sell"))
admin.add_view(ImportView(name="Import"))
admin.add_view(ManagerView(Login, db.session))
admin.add_view(ManagerView(Employee, db.session))
admin.add_view(ManagerView(Supplier, db.session))
admin.add_view(ManagerView(Publisher, db.session))
admin.add_view(ManagerView(Books, db.session))
admin.add_view(ManagerView(Categories, db.session))
admin.add_view(ChangeRegulateView(Regulations, db.session))
admin.add_view(LogoutView(name='Log Out'))
