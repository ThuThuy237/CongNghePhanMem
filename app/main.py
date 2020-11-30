from app import login
from flask_login import login_user
from flask import flash
from app.admin import *
from app.models import Login
from app.utils import check_login


@app.route('/')
def index():
    return render_template('index.html')


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


if __name__ == '__main__':
    app.run(debug=True)
