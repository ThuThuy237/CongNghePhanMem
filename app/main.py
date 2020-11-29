from app import app, login
from flask_login import login_user, AnonymousUserMixin
from flask import render_template, request, flash
from app.admin import *
import hashlib


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/login-admin/", methods=["get", "post"])
def login_admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password', "")
        # loc lai
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        user = Login.query.filter(Login.username == username.strip(),
                                  Login.password == password).first()

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
