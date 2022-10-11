from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlechemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_gravatar import Gravatar
import os

# Creating a Flask instance
app = Flask(__name__)
app.config["SECRET_KEY"] = "SecretKey"

# Connect to the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("TRUE_DATABASE_URL",  "sqlite:///shop.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlechemy(app)

# Introducing login manager
login_manger = LoginManager()
login_manger.init_app(app)

# Inserting Gravatar, a random avatar generator
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)

# Setting out tables. One for users, one for items for sale, one for current orders

class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    description = db.Column(db.Text, unique=False, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    # 5 digits overall in price, 2 digits to be after the decimal point
    price = db.Column(db.Numeric(5, 2), unique=False, nullable=False)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(1000))
    name = db.Column(db.String(1000))
    orders = db.relationship('BlogPost', back_populates="user")


class Orders(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    user = relationship("User", back_populates="orders")
    items = db.relationship("Item", back_populates="name")