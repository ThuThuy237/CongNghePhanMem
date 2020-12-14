import os
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from app import admin, app, utils, db
from flask import redirect, request, session, jsonify
from flask_login import current_user

from app.models import Employee, Login, Supplier, Publisher, Categories, LoginRole, Books


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
                                  password=password, avatar='/static/'+avatar_path):
                    return redirect('/admin/adduserview/')
                else:
                    err_msg = "Hệ thống đang có lỗi! Vui lòng quay lại sau!"
            else:
                err_msg = "Mật khẩu KHÔNG khớp!"

        return self.render('admin/addUser.html', err_msg=err_msg)

    def add(self):
        return self.render('admin/addUser.html')


class SellView(BaseView):
    @expose('/', methods=['get', 'post'])
    def book_by_cate_list(self):
        ut = utils
        cate = utils.read_categories()
        customer = utils.read_customers()
        return self.render('admin/sell.html', ut=ut, cate=cate, customer=customer)

    def add(self):
        return self.render('admin/sell.html')


class ImportView(BaseView):
    @expose('/', methods=['get', 'post'])
    def imp(self):
        supp = utils.read_supplier()
        list_book = utils.read_books()
        cate = utils.read_categories()
        supplier = request.form.get('supplier')
        return self.render('admin/import.html', supp=supp, list_book=list_book, cate=cate)


    def add(self):
        return self.render('admin/import.html')

# class ImportView(BaseView):
#     @expose('/', methods=['get', 'post'])
#     def list_book(self):
#         list_book = utils.read_books()
#         cate = utils.read_categories()
#         supp = utils.read_supplier()
#         return self.render('admin/import.html', list_book=list_book, cate=cate, supp=supp)
#
#     def iport_book(self):
#         name = request.form.get('name')
#         quantity = request.form.get('quantity')
#         categogy = request.form.get('category')
#         author = request.form.get('author')
#         price = request.form.get('price')
#         img = request.file['image']
#
#     def add(self):
#         return self.render('admin/import.html')


class ManagerView(ModelView):
    """
    Nếu tài khoản đăng nhập có login_role == ADMIN thì hiển thị ManagerView
    """

    def is_accessible(self):
        if current_user.is_authenticated:
            if(current_user.login_role == LoginRole.ADMIN):
                return current_user.login_role


admin.add_view(AddUserView(name='Add User'))
admin.add_view(SellView(name="Sell"))
admin.add_view(ImportView(name="Import"))
# admin.add_view(LogoutView(name='Log Out'))
admin.add_view(ManagerView(Login, db.session))
admin.add_view(ManagerView(Employee, db.session))
admin.add_view(ManagerView(Supplier, db.session))
admin.add_view(ManagerView(Publisher, db.session))
admin.add_view(ManagerView(Books, db.session))
