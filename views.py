from flask import render_template, request, redirect, jsonify
from app import app
from modals import *




@app.route("/")
def index():

    return render_template("index.html", products=True, products_= Products.query.all())



@app.route("/orders")
def orders():
    return render_template("orders.html", title='Мої замовлення', orders=True, orders_= Orders.query.all())

@app.route("/product")
def product():
    product_id = request.args.get('id')
    product = Products.query.filter_by(id=product_id).first()
    countrys = Country.query.all()
    citys = City.query.all()
    streets = Streets.query.all()
    return render_template("product.html", title='Товар', product=product, countrys= countrys, citys=citys, streets=streets)


@app.route("/track")
def track():
    return render_template("track.html", title='Відстежити', track=True)


#api
@app.route("/create_order", methods=['POST'])
def create_order():
    product = request.form['product']
    street = request.form['street']
    city = request.form['city']
    country = request.form['country']
    address = Addresses.query.filter_by(country_id = country, city_id = city, street_id= street).first()
    if address == None:
        address = Addresses(country_id = country, city_id = city, street_id= street)
        db.session.add(address)
        db.session.commit()
    order = Orders(product_id = product, addresses_id = address.id, status= StatusType.is_processed)
    db.session.add(order)
    db.session.commit()

    return redirect("/orders")


@app.route("/track_order", methods=['POST'])
def track_order():
    try:
        id_order = request.get_json()['id_order']
        order = Orders.query.filter_by(id=id_order).first()
        if order == None:
            response = {
                "error": f"Замовлення за {id_order} неіснує",
            }
        else:
            response = {
                "result": {
                    "id_order": id_order,
                    "color": order.product_order.color,
                    "weight": order.product_order.weight,
                    "price": order.product_order.price,
                    "address": f"{order.address_order.country.name} {order.address_order.city.name} {order.address_order.street.name}",
                    "status": order.status.value
                },
            }
        return jsonify(response)
    except:
        response = {
            "error": f"Щось пішло не так",
        }

        return jsonify(response)



