import os
import datetime
from flask_admin import BaseView, expose
from flask_admin.model.template import macro
from flask_admin.contrib.sqla import ModelView
from app import admin, app, utils, db
from flask import redirect, request, session
from flask_login import current_user, logout_user
from app.models import *
# from app.models import Employee, Login, Supplier, Publisher, Categories, LoginRole, Books, Regulations, Debtor


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
        customer = utils.read_customers()
        date_sell = datetime.datetime.now()
        date_sell = date_sell.strftime("%d - %B - %Y")
        return self.render('admin/sell.html', list_book=list_book, customer=customer, date_sell=date_sell)


class ImportView(BaseView):
    @expose('/', methods=['get', 'post'])
    def imp(self):
        list_book = utils.read_books()
        supplier = utils.read_supplier()
        date_buy = datetime.datetime.now()
        date_buy = date_buy.strftime("%d - %B - %Y")
        return self.render('admin/import.html', list_book=list_book, supplier=supplier, date_buy=date_buy)

    def add(self):
        return self.render('admin/import.html')


class CollectDebtView(BaseView):
    @expose('/', methods=['get', 'post'])
    def imp(self):
        customer = utils.read_customers()
        date_collect = datetime.datetime.now()
        date_collect = date_collect.strftime("%d - %B - %Y")

        cus_name = request.args.get('customer')
        total = request.args.get('total')
        debtor_id = utils.read_customers(cus_name)
        utils.detele_debt(cus_id=debtor_id, total=total)

        return self.render('admin/collect.html', customer=customer, date=date_collect)

    def add(self):
        return self.render('admin/collect.html')




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
    column_editable_list = ['inventory_max_when_import', 'inventory_min_when_sell', 'import_min', 'debt_max', 'active']
    column_exclude_list = ('login')


class LogoutView(BaseView):
    @expose('/')
    def __index__(self):
        user = current_user
        user.authenticated = False
        session.clear()
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(CollectDebtView(name="Collect Debt"))
admin.add_view(SellView(name="Sell"))
admin.add_view(ImportView(name="Import"))
admin.add_view(ManagerView(Login, db.session))
admin.add_view(ManagerView(Employee, db.session))
admin.add_view(ManagerView(DebtReport, db.session))
admin.add_view(ManagerView(Publisher, db.session))
admin.add_view(ManagerView(Books, db.session))
admin.add_view(ManagerView(Categories, db.session))
admin.add_view(ManagerView(Debtor, db.session))
admin.add_view(ManagerView(Customer, db.session))
admin.add_view(ChangeRegulateView(Regulations, db.session))
admin.add_view(LogoutView(name='Log Out'))
