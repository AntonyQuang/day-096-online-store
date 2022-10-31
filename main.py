from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user, login_manager
from flask_gravatar import Gravatar
from forms import CreateItemForm, RegisterForm, LogInForm
import os
from werkzeug.security import generate_password_hash, check_password_hash

# Creating a Flask instance
app = Flask(__name__)
app.config["SECRET_KEY"] = "SecretKey"
# Connect to the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("TRUE_DATABASE_URL", "sqlite:///shop.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Introducing login manager
login_manager = LoginManager(app)
login_manager.init_app(app)


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
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    password = db.Column(db.String(1000))
    address_1 = db.Column(db.String(200), nullable=False)
    address_2 = db.Column(db.String(200))
    postcode = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(200), nullable=False)
    country = db.Column(db.String(200), nullable=False)
    orders = db.relationship('Item', back_populates="user")


class Orders(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    user = relationship("User", back_populates="orders")
    items = db.relationship("Item", back_populates="name")


# As of Flask-SQLAlchemy 3.0, all access to db.engine (and db.session) requires an active Flask application context.
# db.create_all uses db.engine, so it requires an app context.

with app.app_context():
    db.create_all()


# Inserting Gravatar, a random avatar generator
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)



# what does .user_loader do? You will need to provide a user_loader callback. This callback is used to reload the
# user object from the user ID stored in the session. It should take the str ID of a user, and return the
# corresponding user object. Hence below (as taken from the documentation):
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def home():
    # items = Item.query.all()

    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        data = register_form.data
        first_name = data["first_name"]
        last_name = data["last_name"]
        address_1 = data["address_1"]
        if data["address_2"]:
            address_2 = data["address_2"]
        else:
            address_2 = None
        postcode = data["postcode"]
        city = data["city"]
        country = data["country"]

        email = data["email"]
        password = data["password"]
        hashed_and_salted_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            address_1=address_1,
            address_2=address_2,
            postcode=postcode,
            city=city,
            country=country,
            email=email,
            password=hashed_and_salted_password,
        )
        if db.session.query(User).filter(User.email == new_user.email).first():
            flash("You've already signed up with that email, log in instead")
        else:
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('home'))
    return render_template("register.html", form=register_form, logged_in=current_user.is_authenticated,
                           user_id=current_user.get_id())


@app.route('/register', methods=["GET", "POST"])
def login():
    return "hello"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
