import hashlib

from flask import jsonify
from sqlalchemy.orm.sync import update

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
        quan, total, cus_id = utils.sell_cart_stats(cart)
        order = Order(emm_id=current_user.id, total=total, cus_id=cus_id)
        db.session.add(order)
        regu = Regulations.query.filter(Regulations.id == 1).first()
        customer = get_customer_by_id(cus_id)

        for p in list(cart.values()):
            book = get_book_by_id(p["id"])
            db.session.query(Books).filter(Books.id == p["id"]).update({'inventory': Books.inventory - p["quantity"]})
            if (customer.debt[0].total > regu.debt_max) or ((book.inventory - p["quantity"]) < regu.inventory_min_when_sell):
                return False
            detail = OrderDetail(order=order,
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


def add_buy(cart):
    if cart and current_user.is_authenticated:
        quan, total, sup_id = utils.buy_cart_stats(cart)
        buy = Buy(emm_id=current_user.id, total=total, supplier_id=sup_id)
        db.session.add(buy)
        regu = Regulations.query.filter(Regulations.id == 1).first()

        for p in list(cart.values()):
            book = get_book_by_id(p["id"])
            db.session.query(Books).filter(Books.id == p["id"]).update({'inventory': Books.inventory + p["quantity"]})
            if (p["quantity"] < regu.import_min) or (book.inventory > regu.inventory_max_when_import) :
                return False
            detail = BuyDetail(buy=buy,
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


def detele_debt(cus_id, total):
    if current_user.is_authenticated:
        collect_debt = CollectDebts(total=total, cus_id=cus_id)
        db.session.add(collect_debt)
        db.session.query(Debtor).filter(Debtor.customer_id == cus_id).update({'total': Debtor.total - total})

        try:
            db.session.commit()
            return True
        except Exception as ex:
            print(ex)
        return False


def get_cate_by_id(cate_id):
    return Categories.query.get(cate_id)


def get_customer_by_id(cus_id):
    return Customer.query.get(cus_id)


def read_customers(cus_id=None, kw=None):
    customers = Customer.query

    if cus_id:
        customers = customers.filter(Customer.id == cus_id)

    if kw:
        customers = customers.filter(Customer.name.contains(kw))

    return customers.all()


def get_customer_by_name(name):
    return Customer.query.filter(Customer.name == name).first()


def get_top_book_by_cate(cate, top):
    return Books.query.filter(Books.cat_id == cate).limit(top).all()


def read_supplier(kw=None):
    supplier = Supplier.query

    if kw:
        supplier = supplier.filter(Supplier.name.contains(kw))

    return supplier.all()


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


def sell_cart_stats(cart):
    total_quantity, total_amount, cus_id = 0, 0, 1
    if cart:
        for p in cart.values():
            cus_id = p["cus_id"]
            total_quantity = total_quantity + p["quantity"]
            total_amount = total_amount + p["quantity"] * p["price"]

    return total_quantity, total_amount, cus_id


def buy_cart_stats(cart):
    total_quantity, total_amount, sup_id = 0, 0, 1
    if cart:
        for p in cart.values():
            sup_id = p["sup_id"]
            total_quantity = total_quantity + p["quantity"]
            total_amount = total_amount + p["quantity"] * p["price"]

    return total_quantity, total_amount, sup_id


def get_book_by_id(book_id):
    return Books.query.get(book_id)
