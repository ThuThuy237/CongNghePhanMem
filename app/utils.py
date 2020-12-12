import hashlib
from app import utils
from flask_login import current_user

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


def add_order(cart):
    if cart and current_user.is_authenticated:
        quan, total = utils.cart_stats(cart)
        order = Order(emm_id=current_user.id, total=total, cus_id=1)
        db.session.add(order)

        for p in list(cart.values()):
            detail = OrderDetail(order_id=order.id,
                                 book_id=int(p["id"]),
                                 quantity=p["quantity"],
                                 price=p["price"])
            db.session.add(detail)

        try:
            db.session.commit()
            return True
        except Exception as ex:
            print(ex)

    return False


def get_cate_by_id(id=None):
    return Categories.query.filter(Categories.id == id).all()


def read_customers(cus_id=None, kw=None):
    customers = Customer.query

    if cus_id:
        customers = customers.filter(Customer.id == cus_id)

    if kw:
        customers = customers.filter(Customer.name.contains(kw))

    return customers.all()


def read_books(cate_id=None, kw=None, from_price=None, to_price=None):
    books = Books.query

    if cate_id:
        books = books.filter(Books.cat_id == cate_id)

    if kw:
        books = books.filter(Books.name.contains(kw))

    if from_price and to_price:
        books = books.filter(Books.price.__gt__(from_price),
                             Books.price.__lt__(to_price))

    # return books.first()
    return books.all()


def read_categories(kw=None):
    categories = Categories.query

    if kw:
        categories = categories.filter(Categories.name.contains(kw))

    return categories.all()


def cart_stats(cart):
    total_quantity, total_amount = 0, 0
    if cart:
        for p in cart.values():
            total_quantity = total_quantity + p["quantity"]
            total_amount = total_amount + p["quantity"] * p["price"]

    return total_quantity, total_amount


def get_book_by_id(book_id):
    return Books.query.get(book_id)
