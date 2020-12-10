from app import login
from flask_login import login_user, login_required, logout_user
from flask import flash, render_template
from app.admin import *
from app.models import Login
from app.utils import check_login


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
    logout_user()
    return redirect('/admin')


@app.route('/')
def book_list():
    cat_id = request.args.get('cat_id')
    kw = request.args.get('kw')
    from_price = request.args.get('from_price')
    to_price = request.args.get('to_price')
    books = utils.read_books(cate_id=cat_id, kw=kw, from_price=from_price, to_price=to_price)

    return render_template('list-book.html', books=books)


# @app.route("/admin/sellview/")
# def book_by_cate_list():
#     books = utils.read_books(kw='a')
#     a = 'haha'
#     return render_template('sell.html', books=books, a=a)


if __name__ == '__main__':
    app.run(debug=True)
