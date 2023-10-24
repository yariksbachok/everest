from flask import Flask
from modals import *
from utils import make_celery
from tasks import chek_status_order, r

app = Flask(__name__)
app.config.from_pyfile('config.py')


db.init_app(app)
db.session.expire_on_commit = False

celery = make_celery(app)
celery.set_default()



if __name__ == '__main__':
    r.delete('orders_data')
    chek_status_order.delay()
    from views import *
    from admin import *
    with app.app_context():
        db.create_all()
    app.run()