from app import login
from flask_login import login_user, login_required, logout_user
from flask import flash, render_template,  session, jsonify
from app.admin import *
from app.models import Login
from app.utils import check_login
import json


@app.route("/login-admin/", methods=["get", "post"])
def login_admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password', "")
        user = check_login(username=username, password=password)

        if user:
            login_user(user=user)

    if current_user.is_authenticated:
        pass
    else:
        flash('Login Fail')
    return redirect('/admin')


@login.user_loader
def user_load(user_id):
    return Login.query.get(user_id)


@app.route("/logout")
@login_required
def log_out():
    user = current_user
    user.authenticated = False
    session.clear()
    logout_user()
    return redirect('/admin')


@app.route('/')
def index():
    books = utils.read_books()
    ut = utils
    cate = utils.read_categories()
    return render_template('index.html', books=books, ut=ut, cate=cate)

@app.route('/book-list', methods=["get", "post"])
def book_list():
    cat_id = request.args.get('cat_id')
    kw = request.args.get('kw')
    from_price = request.args.get('from_price')
    to_price = request.args.get('to_price')
    books = utils.read_books(cate_id=cat_id, kw=kw, from_price=from_price, to_price=to_price)
    ut = utils
    cate = utils.read_categories()

    return render_template('list-book.html', books=books, ut=ut, cate=cate)


@app.route('/api/cart', methods=["get", "post"])
def customer_cart():
    if 'customer_cart' not in session:
        session['customer_cart'] = {}

    customer_cart = session['customer_cart']

    data = request.json
    id = str(data.get("id"))
    name = data.get("name")
    price = data.get("price")

    if id in customer_cart:
        customer_cart[id]["quantity"] = customer_cart[id]["quantity"] + 1
    else:
        customer_cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1
        }

    session['customer_cart'] = customer_cart

    quan, price = utils.cart_stats(customer_cart)

    return jsonify({
        "total_amount": price,
        "total_quantity": quan
    })


@app.route('/api/sellcart', methods=["get", "post"])
def sellcart():
    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']

    data = request.json
    id = str(data.get("id"))
    cus_id = str(data.get("cus_id"))
    book = utils.get_book_by_id(id)
    name = book.name
    price = book.price

    if id in cart:
        cart[id]["quantity"] = cart[id]["quantity"] + 1
    else:
        cart[id] = {
            "cus_id": cus_id,
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1
        }

    session['cart'] = cart

    quan, price, cus_id = utils.sell_cart_stats(cart)

    return jsonify({
        "total_amount": price,
        "total_quantity": quan
    })


@app.route('/api/buy-cart', methods=["get", "post"])
def buy_cart():
    if 'buy_cart' not in session:
        session['buy_cart'] = {}

    buy_cart = session['buy_cart']

    data = request.json
    id = str(data.get("id"))
    sup_id = str(data.get("sup_id"))
    quantity = str(data.get("quantity"))
    book = utils.get_book_by_id(id)
    name = book.name
    price = book.import_price

    if id in buy_cart:
        buy_cart[id]["quantity"] = buy_cart[id]["quantity"] + 1
    else:
        buy_cart[id] = {
            "id": id,
            "sup_id": sup_id,
            "name": name,
            "price": price,
            "quantity": 1
        }

    session['buy_cart'] = buy_cart

    quan, price, sup_id = utils.buy_cart_stats(buy_cart)

    return jsonify({
        "total_amount": price,
        "total_quantity": quan
    })


@app.route('/payment')
def payment():
    quan, price = utils.cart_stats(session.get('cart'))
    cart_info = {
        "total_amount": price,
        "total_quantity": quan
    }
    return render_template('payment.html',
                           cart_info=cart_info)


@app.route('/api/submit-order', methods=['post'])
def submit_order():
    if utils.add_order(session.get('cart')):
        del session['cart']
        return jsonify({'message': 'Add order successful!'})

    return jsonify({'message': 'failed'})


@app.route('/api/submit-buy', methods=['post'])
def submit_buy():
    if utils.add_buy(session.get('buy_cart')):
        del session['buy_cart']
        return jsonify({'message': 'Add buy successful!'})

    return jsonify({'message': 'failed'})


# @app.route('/admin/iportview', methods=["get", "post"])
# def iport_book():
#     name = request.form.get('name')
#     quantity = request.form.get('quantity')
#     categogy = request.form.get('category')
#     author = request.form.get('author')
#     price = request.form.get('price')
#     img = request.file['image']




if __name__ == '__main__':
    app.run(debug=True)
