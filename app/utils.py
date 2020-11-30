import hashlib

from app import db
from app.models import Login, LoginRole


def check_login(username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    user = Login.query.filter(Login.username == username,
                             Login.password == password).first()

    return user


def add_user(name, username, email, password, avatar, ):
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
