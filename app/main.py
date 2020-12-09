from app import login
from flask_login import login_user
from flask import flash
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
    return redirect('/')


@login.user_loader
def user_load(user_id):
    return Login.query.get(user_id)


@app.route("/admin/adduserview/", methods=['get', 'post'])
def register():
    err_msg = ""
    if request.method == 'POST':
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if password == confirm:
            name = request.form.get('name')
            email = request.form.get('email')
            username = request.form.get('username')
            avatar = request.files["avatar"]

            avatar_path = 'images/upload/%s' % avatar.filename
            avatar.save(os.path.join(app.root_path,
                                     'static/',
                                     avatar_path))
            if utils.add_user(name=name, email=email, username=username,
                              password=password, avatar=avatar_path):
                return redirect('/')
            else:
                err_msg = "Hệ thống đang có lỗi! Vui lòng quay lại sau!"
        else:
            err_msg = "Mật khẩu KHÔNG khớp!"

    return render_template('addUser.html', err_msg=err_msg)


@app.route('/')
def book_list():
    cat_id = request.args.get('cat_id')
    kw = request.args.get('kw')
    from_price = request.args.get('from_price')
    to_price = request.args.get('to_price')
    books = utils.read_books(cate_id=cat_id, kw=kw, from_price=from_price, to_price=to_price)

    return render_template('list-book.html', books=books)


if __name__ == '__main__':
    app.run(debug=True)
