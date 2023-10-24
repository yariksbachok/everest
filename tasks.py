from celery import shared_task
from modals import *
import redis
import json
from datetime import datetime
import config

r = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)

def write_log(id, status):
    log_file = open("log.txt", "a", encoding='utf-8')
    log_file.write(str(datetime.now()) + ': ' + f"Замовлення %{id}% змінило статус на %{status}%" + '\n')
    log_file.close()

def create_temp_orders():
    orders = Orders.query.all()
    data_to_store = [order.to_dict() for order in orders]

    r.set('orders_data', json.dumps(data_to_store))

@shared_task()
def chek_status_order():
    temp_orders = r.get('orders_data')
    if temp_orders is None:
        create_temp_orders()
    else:
        temp_orders = json.loads(temp_orders)
        for order in temp_orders:
            now_status_order = Orders.query.filter_by(id=order["id"]).first().status.value
            if order["status"] != now_status_order:
                write_log(order["id"], now_status_order)
                create_temp_orders()
        create_temp_orders()