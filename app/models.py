from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Float, String, ForeignKey, Enum
from sqlalchemy.orm import relationship, backref
from app import db
from flask_login import UserMixin
from enum import Enum as dbEnum


class InforBase(db.Model):
    __abstract__ = True

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    name = Column(String(50), nullable=False)


class UserBase(InforBase):
    __abstract__ = True

    gender = Column(String(10))
    birthday = Column(String(50))
    address = Column(String(255))
    phone = Column(String(15))


class Customer(UserBase):
    __tablename__ = 'customer'

    order = relationship('Order', backref='customer', lazy=True)

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
    price = Column(Float, nullable=False)  # Gia
    image = Column(String(100))  # Hinh anh
    cat_id = Column(Integer, ForeignKey(Categories.id), nullable=False)
    publisher_id = Column(Integer, ForeignKey(Publisher.id), nullable=False)

    def __str__(self):
        return self.name


class Order(db.Model):
    __tablename__ = 'order'

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.today())
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
    date = Column(DateTime, default=datetime.today())
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


if __name__ == '__main__':
    db.create_all()
