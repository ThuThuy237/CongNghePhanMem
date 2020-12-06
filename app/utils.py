import hashlib
from app.models import *


def check_login(username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    user = Login.query.filter(Login.username == username,
                              Login.password == password).first()

    return user


def add_user(name, username, email, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = Login(name=name, email=email,
              username=username, password=password,
              avatar=avatar)
    try:
        db.session.add(u)
        db.session.commit()
        return True
    except Exception as ex:
        print(ex)
        return False


def get_user_by_id(user_id):
    return Login.query.get(user_id)


def read_customers(cus_id=None, kw=None):
    customers = Customer.query

    if cus_id:
        customers = customers.filter(Customer.id == cus_id)

    if kw:
        customers = customers.filter(Customer.name.contains(kw))

    return customers.all()


def read_books(book_id=None, kw=None, from_price=None, to_price=None):
    books = Books.query

    if book_id:
        books = books.filter(Books.id == book_id)

    if kw:
        books = books.filter(Books.name.contains(kw))

    if from_price and to_price:
        books = books.filter(Books.price.__gt__(from_price),
                             Books.price.__lt__(to_price))

    return books.all()


def get_book_by_id(book_id):
    return Books.query.get(book_id)