from app import login
from flask_login import login_user, login_required, logout_user
from flask import flash, render_template,  session, jsonify
from app.admin import *
from app.models import Login
from app.utils import check_login
import json


# @app.route('/')
# def index():
#     return render_template('index.html')


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


@app.route('/', methods=["get", "post"])
def book_list():
    cat_id = request.args.get('cat_id')
    kw = request.args.get('kw')
    from_price = request.args.get('from_price')
    to_price = request.args.get('to_price')
    books = utils.read_books(cate_id=cat_id, kw=kw, from_price=from_price, to_price=to_price)

    return render_template('list-book.html', books=books)


@app.route('/api/cart', methods=["get", "post"])
def cart():
    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']

    data = request.json
    id = str(data.get("id"))
    name = data.get("name")
    price = data.get("price")

    if id in cart:
        cart[id]["quantity"] = cart[id]["quantity"] + 1
    else:
        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1
        }

    session['cart'] = cart

    quan, price = utils.cart_stats(cart)

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
    name = data.get("name")
    price = data.get("price")

    if id in cart:
        cart[id]["quantity"] = cart[id]["quantity"] + 1
    else:
        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1
        }

    session['cart'] = cart

    quan, price = utils.cart_stats(cart)

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


@app.route('/api/pay', methods=['post'])
def pay():
    if utils.add_order(session.get('cart')):
        del session['cart']
        return jsonify({'message': 'Add receipt successful!'})

    return jsonify({'message': 'failed'})


if __name__ == '__main__':
    app.run(debug=True)
