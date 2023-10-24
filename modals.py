from flask_sqlalchemy import SQLAlchemy
import enum
from datetime import datetime
from flask_login import UserMixin
from flask_security import RoleMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

#модель продуктів
class Products(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float, nullable= True)
    color = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Integer, nullable=True)
    address = db.relationship('Orders', backref='product_order', lazy='dynamic')

    def __repr__(self):
        return f"product {self.id} / {self.weight} / {self.price} / {self.color}"

#модель країн
class Country(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    cities = db.relationship('City', backref='country', lazy=True)
    def __repr__(self):
        return (self.name)

class City(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    streets = db.relationship('Streets', backref='city', lazy=True)

    def __repr__(self):
        return (self.name)

#модель вулиць
class Streets(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)

    def __repr__(self):
        return f"street {self.name}"

#модель адресів
class Addresses(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    street_id = db.Column(db.Integer, db.ForeignKey('streets.id'), nullable=False)

    street = db.relationship('Streets', backref='addresses', uselist=False)
    city = db.relationship('City', backref='addresses', uselist=False)
    country = db.relationship('Country', backref='addresses', uselist=False)

    address = db.relationship('Orders', backref='address_order', lazy=True)


    def __repr__(self):
        return f"address {self.street} / {self.city} / {self.country}"

    @staticmethod
    def create_address(street_id, city_id, country_id, other_data):
        street = Streets.query.filter_by(id=street_id, city_id=city_id).first()
        if street and street.city_id == city_id:
            city = City.query.filter_by(id=city_id, country_id=country_id).first()
            if city and city.country_id == country_id:
                new_address = Addresses(street_id=street_id, city_id=city_id, country_id=country_id, other_data=other_data)
                db.session.add(new_address)
                db.session.commit()
                return new_address
        return None


class StatusType(enum.Enum):
    done = "Done"
    canceled = "Canceled"
    is_processed = "Is processed"

#модель замовлень
class Orders(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(StatusType), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    addresses_id = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'status': self.status.value
        }

    def __repr__(self):
        return f"order {self.id} -> {self.status}"

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'))
)


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    # Flask - Login
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    # Flask-Security
    def has_role(self, *args):
        return set(args).issubset({role.name for role in self.roles})

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


