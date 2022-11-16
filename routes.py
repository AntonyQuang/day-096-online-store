from flask import render_template, session, request, url_for, flash, redirect
from forms import RegistrationForm, LoginForm, AddProductsForm
from __init__ import app, db, bcrypt
from models import User, Brand, Category


@app.route('/')
def home():
    return render_template('index.html', title="Admin Page")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data,
                    username=form.username.data,
                    email=form.email.data,
                    password=hash_password,
                    )
        with app.app_context():
            db.session.add(user)
            db.session.commit()
        flash(f"Welcome {form.name.data}, thank you for registering", "success")
        return redirect(url_for('home'))
    return render_template('register.html', form=form, title="Registration Page")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session["email"] = form.email.data
            flash(f"Welcome {form.email.data}. You are now logged in.", "success")
            return redirect(request.args.get('next') or url_for("admin"))
        else:
            flash("The email or password is not correct. Please try again", "danger")
    return render_template('login.html', form=form, title="Login Page")


@app.route('/addbrand', methods=["GET", "POST"])
def addbrand():
    if request.method == "POST":
        getbrand = request.form.get("brand")
        print(getbrand)
        brand = Brand(name=getbrand)
        flash(f"The Brand {getbrand} has been added to your database.", "success")
        with app.app_context():
            db.session.add(brand)
            db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('addbrand.html', brands="brands")


@app.route('/addcat', methods=["GET", "POST"])
def addcat():
    if request.method == "POST":
        getcat = request.form.get("category")
        print(getcat)
        cat = Category(name=getcat)
        flash(f"The Category {getcat} has been added to your database.", "success")
        with app.app_context():
            db.session.add(cat)
            db.session.commit()
        return redirect(url_for('addbrand'))
    return render_template('addbrand.html')


@app.route("/addproduct", methods=["GET", "POST"])
def addproduct():
    brands = Brand.query.all()
    categories = Category.query.all()
    form = AddProductsForm(request.form)
    return render_template("addproduct.html", form=form, title="Add product", brands=brands, categories=categories)