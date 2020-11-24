from sqlalchemy import Column, Integer, DateTime, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app import db


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


class Login(db.Model):
    __tablename__ = 'login'

    name = Column(String(20), nullable=False, primary_key=True)
    password = Column(String(20), nullable=False)
    access = Column(String(20), nullable=False)
    employee = relationship('Employee', backref='login', lazy=True, uselist=False)


class Employee(InforBase):
    __tablename__ = 'employee'

    title = Column(String(20), nullable=False)
    hireDate = Column(DateTime, nullable=False)
    userName = Column(String(20), ForeignKey(Login.name), nullable=False)


class Categories(InforBase):
    __tablename__ = 'categories'

    describe = Column(String(255))
    books = relationship('Books', backref='categories', lazy=True)


class Publisher(InforBase):
    __tablename__ = 'publisher'

    address = Column(String(255))
    phone = Column(String(20))


class Supplier(InforBase):
    __tablename__ = 'supplier'

    address = Column(String(255))
    phone = Column(String(20))


class Books(InforBase):
    __tablename__ = 'books'

    author = Column(String(50), nullable=False)
    inventory = Column(Integer, nullable=False)
    cat_id = Column(Integer, ForeignKey(Categories.id), nullable=False)
    publisher_id = Column(Integer, ForeignKey(Publisher.id), nullable=False)


class Order(db.Model):
    __tablename__ = 'order'

    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    date = Column(DateTime, nullable=False)
    total = Column(Float, nullable=False)
    emm_id = Column(Integer, ForeignKey(Employee.id), nullable=False)
    cus_id = Column(Integer, ForeignKey(Customer.id), nullable=False)


orderDetai = db.Table('orderditail',
                      Column('bookId', Integer, ForeignKey(Books.id), primary_key=True),
                      Column('orderId', Integer, ForeignKey(Order.id), primary_key=True))
'''class OrderDetail(db.Model):
    __tablename__ = 'orderdetail'

    order_id = Column(Integer,ForeignKey(Order.id), nullable=False, primary_key=True)
    book_id = Column(Integer, ForeignKey(Books.id), nullable=False, primary_key=True)
    price = Column(Float, nullable=False)'''


if __name__ == '__main__':
    db.create_all()
