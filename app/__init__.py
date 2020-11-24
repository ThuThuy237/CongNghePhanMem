from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://root:12345@localhost/mydb?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= True

db = SQLAlchemy(app = app)
admin = Admin(app =app, name='Administrator',template_mode="bootstrap4")