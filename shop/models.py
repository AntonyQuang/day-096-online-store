from shop import db, login_manager
from shop import app
from datetime import datetime
from flask_login import UserMixin
import sqlalchemy.types as types
import json

class SqliteNumeric(types.TypeDecorator):
    impl = types.String
    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(types.VARCHAR(100))
    def process_bind_param(self, value, dialect):
        return str(value)
    def process_result_value(self, value, dialect):
        return D(value)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)
    password = db.Column(db.String(180), unique=False, nullable=False)
    profile = db.Column(db.String(180), unique=False, nullable=False, default="profile.jpg")


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)


class AddProduct(db.Model):
    __searchable__ = ["name", "description"]
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable=False)
    colors = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    brand = db.relationship('Brand', backref=db.backref('brands', lazy=True))

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('posts', lazy=True))

    image_1 = db.Column(db.String(150), nullable=False, default="image.jpg")
    image_2 = db.Column(db.String(150), nullable=False, default="image.jpg")
    image_3 = db.Column(db.String(150), nullable=False, default="image.jpg")

    def __repr__(self):
        return "<AddProduct %r>" % self.name

@login_manager.user_loader
def user_loader(user_id):
    return Customer.query.get(user_id)

class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(180), unique=False, nullable=False)
    country = db.Column(db.String(50), unique=False, nullable=False)
    state = db.Column(db.String(50), unique=False)
    city = db.Column(db.String(50), unique=False, nullable=False)
    contact = db.Column(db.String(30), unique=False)
    address_1 = db.Column(db.String(80), unique=False, nullable=False)
    address_2 = db.Column(db.String(80), unique=False)
    zipcode = db.Column(db.String(30), unique=False, nullable=False)
    profile = db.Column(db.String(180), unique=False, default="profile.jpg")
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "<Customer %r>" % self.name


class JsonEncodedDict(db.TypeDecorator):
    impl = db.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.loads(value)


class CustomerOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default="Pending", nullable=False)
    customer_id = db.Column(db.Integer, unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    orders = db.Column(JsonEncodedDict)

    def __repr__(self):
        return "<CustomerOrder %r>" % self.invoice


with app.app_context():
    db.create_all()
    db.session.commit()