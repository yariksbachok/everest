
from flask import url_for, redirect
from modals import *
import flask_login as login
from flask_security import SQLAlchemyUserDatastore, Security, current_user
import flask_admin
from flask_admin import helpers, expose
from flask_admin.contrib import sqla
from app import app
from .routes import admin_bp

app.register_blueprint(admin_bp, url_prefix="/admin")


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)





# Create customized model view class
class MyModelView(sqla.ModelView):

    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated)

    def _handle_view(self, name):
        if not self.is_accessible():
            return redirect(url_for('security.login'))


class MyAdminIndexView(flask_admin.AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('.login_page'))
        return super(MyAdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_page(self):
        if current_user.is_authenticated:
            return redirect(url_for('.index'))
        return super(MyAdminIndexView, self).index()

    @expose('/logout/')
    def logout_page(self):
        login.logout_user()
        return redirect(url_for('.index'))

    @expose('/reset/')
    def reset_page(self):
        return redirect(url_for('.index'))


# Create admin
admin = flask_admin.Admin(app, index_view=MyAdminIndexView(), base_template='admin/master-extended.html')

# Add view
admin.add_view(MyModelView(Products, db.session, name="Товари"))
admin.add_view(MyModelView(Country, db.session, name="Країни"))
admin.add_view(MyModelView(City, db.session, name="Міста"))
admin.add_view(MyModelView(Streets, db.session, name="Вулиці"))
admin.add_view(MyModelView(Addresses, db.session, name="Адреси"))
admin.add_view(MyModelView(Orders, db.session, name="Замовлення"))



# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=helpers,
        get_url=url_for
    )