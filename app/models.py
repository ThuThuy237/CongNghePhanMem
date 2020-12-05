from sqlalchemy import Column, Integer, DateTime, Float, String, ForeignKey, Enum
from sqlalchemy.orm import relationship, backref
from app import db
from flask_login import UserMixin
from enum import Enum as LoginEnum


class InforBase(db.Model):
    __abstract__ = True

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    name = Column(String(50), nullable=False)


class UserBase(InforBase):
    __abstract__ = True

    gender = Column(String(10), nullable=False)
    birthday = Column(DateTime, nullable=False)
    address = Column(String(255))
    phone = Column(String(15), )


class Customer(UserBase):
    __tablename__ = 'customer'

    order = relationship('Order', backref='customer', lazy=True)


class LoginRole(LoginEnum):
    ADMIN = 1
    USER = 2


class Login(db.Model, UserMixin):
    __tablename__ = 'login'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(50))
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    avatar = Column(String(100))
    login_role = Column(Enum(LoginRole), default=LoginRole.USER)
    # employee = relationship('Employee', backref='login', lazy=True, uselist=False)

    def __str__(self):
        return self.name


class Employee(InforBase):
    __tablename__ = 'employee'

    title = Column(String(20), nullable=False)
    hireDate = Column(DateTime, nullable=False)
    userid = Column(Integer, ForeignKey(Login.id), unique=True)
    account = relationship('Login', backref='employee', lazy=True, uselist=False)
    oder = relationship('Order', backref='employee', lazy=True)
    buy = relationship('Buy', backref='employee', lazy=True)

    def __str__(self):
        return self.name


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

    author = Column(String(50), nullable=False)  # Tác
    inventory = Column(Integer, nullable=False)  # lượng hàng
    price = Column(Float, nullable=False)  # Gi
    cat_id = Column(Integer, ForeignKey(Categories.id), nullable=False)
    publisher_id = Column(Integer, ForeignKey(Publisher.id), nullable=False)

    def __str__(self):
        return self.name

    suppliers = relationship('Supplier',
                             secondary='buy_detail',
                             lazy='subquery',
                             backref=backref('books', lazy=True))


class Order(db.Model):
    __tablename__ = 'order'

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    date = Column(DateTime, nullable=False)
    total = Column(Float, nullable=False)
    emm_id = Column(Integer, ForeignKey(Employee.id), nullable=False)
    cus_id = Column(Integer, ForeignKey(Customer.id), nullable=False)

    def __str__(self):
        return self.name

    books = relationship('Books',
                         secondary='order_detail',
                         lazy='subquery',
                         backref=backref('order', lazy=True))


order_detai = db.Table('order_detail',
                       Column('bookId', Integer, ForeignKey(Books.id), primary_key=True),
                       Column('orderId', Integer, ForeignKey(Order.id), primary_key=True),
                       Column('quantity', Integer, nullable=False))


class Buy(db.Model):
    __tablename__ = 'buy'
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    date = Column(DateTime, nullable=False)
    total = Column(Float, nullable=False)
    supplier_id = Column(Integer, ForeignKey(Supplier.id), nullable=False)
    emm_id = Column(Integer, ForeignKey(Employee.id), nullable=False)

    def __str__(self):
        return self.name


buy_detail = db.Table('buy_detail',
                      Column('supplierId', Integer, ForeignKey(Supplier.id), nullable=False, primary_key=True),
                      Column('bookId', Integer, ForeignKey(Books.id), nullable=False, primary_key=True),
                      Column('quantity', Integer, nullable=False))

if __name__ == '__main__':
    db.create_all()
