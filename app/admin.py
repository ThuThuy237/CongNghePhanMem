from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from app import admin, db
from app.models import  *

class ContactView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/contact.html')


admin.add_view(ModelView(Login, db.session))
admin.add_view(ModelView(Customer, db.session))
admin.add_view(ModelView(Employee, db.session))
admin.add_view(ModelView(Categories, db.session))
admin.add_view(ModelView(Publisher, db.session))
admin.add_view(ModelView(OrderDetail, db.session))
admin.add_view(ModelView(Order, db.session))
admin.add_view(ModelView(Supplier, db.session))
admin.add_view(ModelView(Books, db.session))
admin.add_view(ContactView(name='Log in'))