from datetime import datetime as modelDateTime
from sqlalchemy import Column, Integer, DateTime, Float, String, ForeignKey, Enum, Numeric, Boolean, Date
from sqlalchemy.orm import relationship, backref
from app import db
from flask_login import UserMixin
from enum import Enum as dbEnum


class InforBase(db.Model):
    __abstract__ = True

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    name = Column(String(150), nullable=False)


class UserBase(InforBase):
    __abstract__ = True

    gender = Column(String(10))
    birthday = Column(String(50))
    address = Column(String(255))
    phone = Column(String(15))


class Customer(UserBase):
    __tablename__ = 'customer'

    order = relationship('Order', backref='customer', lazy=True)
    collect_debts = relationship('CollectDebts', backref='customer', lazy=True)  #phieu thu no
    debt = relationship('Debtor', backref='customer', lazy=True)  # tong tien no
    debt_report = relationship('DebtReport', backref='customer', lazy=True)

    def __str__(self):
        return self.name


class LoginRole(dbEnum):
    ADMIN = 1
    USER = 2


class TitleRole(dbEnum):
    CASHIER = 1
    STAFF = 2
    MANAGER = 3


class Employee(db.Model):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    title = Column(Enum(TitleRole), default=TitleRole.STAFF)
    hireDate = Column(String(50))
    account = relationship('Login', backref='employee', lazy=True, uselist=False)
    oder = relationship('Order', backref='employee', lazy=True)
    buy = relationship('Buy', backref='employee', lazy=True)

    def __str__(self):
        return self.name


class Login(db.Model, UserMixin):
    __tablename__ = 'login'

    id = Column(Integer, ForeignKey(Employee.id), nullable=False, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    avatar = Column(String(100))
    login_role = Column(Enum(LoginRole), default=LoginRole.USER)
    reg = relationship('Regulations', backref="login", lazy=True)

    def __str__(self):
        return self.employee.name


class Categories(InforBase):
    __tablename__ = 'categories'

    describe = Column(String(255))
    books = relationship('Books', backref='categories', lazy=True)

    def __str__(self):
        return self.name


# Nhà xuất bản
class Publisher(InforBase):
    __tablename__ = 'publisher'

    address = Column(String(255))
    phone = Column(String(20))
    books = relationship('Books', backref='publisher', lazy=True)

    def __str__(self):
        return self.name


# Nhà cung cấp
class Supplier(InforBase):
    __tablename__ = 'supplier'

    address = Column(String(255))
    phone = Column(String(20))
    buy = relationship('Buy', backref='supplier', lazy=True)

    def __str__(self):
        return self.name


class Books(InforBase):
    __tablename__ = 'books'

    author = Column(String(50), nullable=False)  # Tác gia
    inventory = Column(Integer, nullable=False)  # lượng hàng
    import_price = Column(Float, nullable=False) # Gia nhap
    price = Column(Float, default=import_price + import_price * 0.25)  # Gia ban
    image = Column(String(300))  # Hinh anh
    cat_id = Column(Integer, ForeignKey(Categories.id), nullable=False)
    publisher_id = Column(Integer, ForeignKey(Publisher.id), nullable=False)

    def __str__(self):
        return self.name


class Order(db.Model):
    __tablename__ = 'order'

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    date = Column(DateTime, nullable=False, default=modelDateTime.today())
    total = Column(Float, nullable=False)
    emm_id = Column(Integer, ForeignKey(Employee.id), nullable=False)
    cus_id = Column(Integer, ForeignKey(Customer.id))
    detail = relationship('OrderDetail', backref='order', lazy=True)

    books = relationship('Books',
                         secondary='order_detail',
                         lazy='subquery',
                         backref=backref('order', lazy=True))


class OrderDetail(db.Model):
    __tablename__ = 'order_detail'

    id = Column(Integer, autoincrement=True, primary_key=True)
    book_id = Column(Integer, ForeignKey(Books.id))
    order_id = Column(Integer, ForeignKey(Order.id))
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)

    def __str__(self):
        return self.name


class Buy(db.Model):
    __tablename__ = 'buy'
    id = Column(Integer, autoincrement=True, primary_key=True)
    date = Column(DateTime, default=modelDateTime.today())
    total = Column(Float, nullable=False)
    supplier_id = Column(Integer, ForeignKey(Supplier.id))
    emm_id = Column(Integer, ForeignKey(Employee.id), nullable=False)
    detail = relationship('BuyDetail', backref='buy', lazy=True)

    def __str__(self):
        return self.name


class BuyDetail(db.Model):
    __tablename__ = 'buy_detail'

    id = Column(Integer, autoincrement=True, primary_key=True)
    book_id = Column(Integer, ForeignKey(Books.id))
    buy_id = Column(Integer, ForeignKey(Buy.id))
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)


#quy dinh
class Regulations(db.Model):
    __tablename__ = 'regulations'

    id = Column(Integer, nullable=False, default=1)
    import_min = Column(Integer, nullable=True, default=150)
    inventory_max_when_import = Column(Integer, nullable=True, default=300)
    inventory_min_when_sell = Column(Integer, nullable=True, default=20)
    debt_max = Column(Numeric, nullable=True, default=20000)
    active = Column(Boolean, default=True)
    id_user = Column(Integer, ForeignKey(Login.id),primary_key=True, nullable=False)


#so luong sach ton
class InventoryReport(db.Model):
    __tablename__ = "inventory_report"
    id = Column(Integer, primary_key=True, autoincrement=True)
    inventory_befor = Column(Numeric, nullable=False) #ton dau
    incurred = Column(Numeric, nullable=False)  #phat sinh
    inventory_after = Column(Numeric, nullable=False) # ton cuoi
    book_id = Column(Integer, ForeignKey(Books.id), nullable=False)


# PhieuThuTienNo
class CollectDebts(db.Model):
    __tablename__ = "collect_debts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, default=modelDateTime.today())
    total = Column(Float, nullable=False)
    cus_id = Column(Integer, ForeignKey(Customer.id), nullable=False)


# BaoCaoCongNo
class DebtReport(db.Model):
    __tablename__ = "debt_report"
    id = Column(Integer, primary_key=True,autoincrement=True)
    month = Column(Date, nullable=False)
    debt_after = Column(Numeric, nullable=False)
    incurred = Column(Numeric, nullable=False)
    cus_id = Column(Integer, ForeignKey(Customer.id), nullable=False)


class Debtor(db.Model):
    __tablename__ = "debtor"
    debt_date = Column(DateTime, default= modelDateTime.today())
    total = Column(Float, nullable=False)
    Customer_id = Column(Integer, ForeignKey(Customer.id), primary_key=True, nullable=False)


if __name__ == '__main__':
    db.create_all()
