from flask import render_template, session, request, url_for, flash, redirect, current_app
from forms import RegistrationForm, LoginForm, AddProductsForm
from __init__ import app, db, bcrypt, photos
from models import User, Brand, Category, AddProduct

import secrets, os



@app.route('/')
def home():
    page = request.args.get('page',1, type=int)
    products = AddProduct.query.filter(AddProduct.stock > 0).paginate(page=page, per_page=1)
    # use the following instead of brands = Brand.query.all() to avoid showing brands with no products
    brands = Brand.query.join(AddProduct, (Brand.id == AddProduct.brand_id)).all()
    categories = Category.query.join(AddProduct, (Category.id == AddProduct.category_id)).all()
    return render_template("products/index.html", title="Home", products=products, brands=brands, categories=categories)


@app.route('/product/<int:id>')
def single_page(id):
    product = AddProduct.query.get_or_404(id)
    categories = Category.query.join(AddProduct, (Category.id == AddProduct.category_id)).all()
    brands = Brand.query.join(AddProduct, (Brand.id == AddProduct.brand_id)).all()
    return render_template("products/single_page.html", product=product, brands=brands, categories=categories)

@app.route('/brands/<int:id>')
def get_brand(id):
    page = request.args.get('page', 1, type=int)
    brand = AddProduct.query.filter_by(brand_id=id).paginate(page=page, per_page=1)
    brand_with_id = Category.query.filter_by(id=id).first_or_404()
    brands = Brand.query.join(AddProduct, (Brand.id == AddProduct.brand_id)).all()
    categories = Category.query.join(AddProduct, (Category.id == AddProduct.category_id)).all()
    return render_template("products/index.html", brand=brand, brands=brands, categories=categories, brand_with_id=brand_with_id)


@app.route('/categories/<int:id>')
def get_category(id):
    page = request.args.get('page',1, type=int)
    category_with_id = Category.query.filter_by(id=id).first_or_404()
    category = AddProduct.query.filter_by(category_id=id).paginate(page=page, per_page=2)
    categories = Category.query.join(AddProduct, (Category.id == AddProduct.category_id)).all()
    brands = Brand.query.join(AddProduct, (Brand.id == AddProduct.brand_id)).all()
    return render_template("products/index.html", category=category, categories=categories, brands=brands, category_with_id=category_with_id)


@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'Please log in first', 'danger')
        return redirect(url_for('login'))
    products = AddProduct.query.all()
    return render_template('admin/index.html', title="Admin Page", products=products)


@app.route('/brands')
def brands():
    if 'email' not in session:
        flash(f'Please log in first', 'danger')
        return redirect(url_for('login'))
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html', title="Brand Page", brands=brands)


@app.route('/categories')
def categories():
    if 'email' not in session:
        flash(f'Please log in first', 'danger')
        return redirect(url_for('login'))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/brand.html', title="Brand Page", categories=categories)


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
        return redirect(url_for('admin'))
    return render_template('admin/register.html', form=form, title="Registration Page")


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
    if 'email' not in session:
        flash(f'Please log in first', 'danger')
        return redirect(url_for('login'))
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


@app.route('/updatebrand/<int:id>', methods=["GET", "POST"])
def updatebrand(id):
    if 'email' not in session:
        flash(f'Please log in first', 'danger')
        return redirect(url_for('login'))
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == "POST":
        updatebrand.name = brand
        db.session.commit()
        flash(f'Your brand has been updated', 'success')
        return redirect(url_for('brands'))
    return render_template('updatebrand.html', title='Update Brand Page', updatebrand=updatebrand)


@app.route('/deletebrand/<int:id>', methods=["POST"])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(brand)
        db.session.commit()
        flash(f'The brand {brand.name} was deleted from your database', 'success')
        return redirect(url_for('admin'))
    flash(f'The brand {brand.name} cannot be deleted', 'warning')
    return redirect(url_for('admin'))

@app.route('/addcat', methods=["GET", "POST"])
def addcat():
    if 'email' not in session:
        flash(f'Please log in first', 'danger')
        return redirect(url_for('login'))
    if request.method == "POST":
        getcat = request.form.get("category")
        print(getcat)
        cat = Category(name=getcat)
        flash(f"The Category {getcat} has been added to your database.", "success")
        with app.app_context():
            db.session.add(cat)
            db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('addbrand.html')


@app.route('/updatecat/<int:id>', methods=["GET", "POST"])
def updatecat(id):
    if 'email' not in session:
        flash(f'Please log in first', 'danger')
        return redirect(url_for('login'))
    updatecat = Category.query.get_or_404(id)
    cat = request.form.get('category')
    if request.method == "POST":
        updatecat.name = cat
        db.session.commit()
        flash(f'Your brand has been updated', 'success')
        return redirect(url_for('categories'))
    return render_template('updatebrand.html', title='Update Category Page', updatecat=updatecat)


@app.route('/deletecat/<int:id>', methods=["POST"])
def deletecat(id):
    category = Category.query.get_or_404(id)
    if request.method == "POST":
        db.session.delete(category)
        db.session.commit()
        flash(f'The category {category.name} was deleted from your database', 'success')
        return redirect(url_for('admin'))
    flash(f'The category {category.name} cannot be deleted', 'warning')
    return redirect(url_for('admin'))


@app.route("/addproduct", methods=["GET", "POST"])
def addproduct():
    brands = Brand.query.all()
    categories = Category.query.all()
    form = AddProductsForm(request.form)
    if request.method == "POST":
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        description = form.description.data
        # brand and category are not part of the AddProducts class
        brand = request.form.get('brand')
        category = request.form.get('category')
        image_1 = photos.save(request.files.get("image_1"), name=secrets.token_hex(10)+".")
        image_2 = photos.save(request.files.get("image_2"), name=secrets.token_hex(10)+".")
        image_3 = photos.save(request.files.get("image_3"), name=secrets.token_hex(10)+".")
        addpro = AddProduct(
            name=name,
            price=price,
            discount=discount,
            stock=stock,
            colors=colors,
            description=description,
            brand_id=brand,
            category_id=category,
            image_1=image_1,
            image_2=image_2,
            image_3=image_3,
        )
        with app.app_context():
            db.session.add(addpro)
            flash(f"The products {name} has been added to the database", "success")
            db.session.commit()
        return redirect(url_for('admin'))
    return render_template("addproduct.html", form=form, title="Add products", brands=brands, categories=categories)


@app.route("/updateproduct/<int:id>", methods=["GET", "POST"])
def updateproduct(id):
    product = AddProduct.query.get_or_404(id)
    brands = Brand.query.all()
    categories = Category.query.all()
    form = AddProductsForm(request.form)
    brand = request.form.get("brand")
    category = request.form.get("category")
    if request.method == "POST":
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.category_id = category
        product.brand_id = brand
        product.colors = form.colors.data
        product.description = form.description.data
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
                product.image_1 = photos.save(request.files.get("image_1"), name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get("image_1"), name=secrets.token_hex(10) + ".")
        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
                product.image_2 = photos.save(request.files.get("image_2"), name=secrets.token_hex(10) + ".")
            except:
                product.image_12 = photos.save(request.files.get("image_2"), name=secrets.token_hex(10) + ".")
        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
                product.image_3 = photos.save(request.files.get("image_3"), name=secrets.token_hex(10) + ".")
            except:
                product.image_3 = photos.save(request.files.get("image_3"), name=secrets.token_hex(10) + ".")
        db.session.commit()
        flash(f'Your products has been updated', "success")
        return redirect(url_for('admin'))
    form.name.data = product.name
    form.price.data = product.price
    form.description.data = product.description
    form.stock.data = product.stock
    form.discount.data = product.discount
    form.colors.data = product.colors
    return render_template("updateproduct.html", form=form, brands=brands, categories=categories, product=product)


@app.route('/deleteproduct/<int:id>', methods=["POST"])
def deleteproduct(id):
    product = AddProduct.query.get_or_404(id)
    if request.method == "POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'The products {product.name} was deleted from your database', 'success')
        return redirect(url_for('admin'))
    flash(f'The products {product.name} cannot be deleted', 'warning')
    return redirect(url_for('admin'))


def mergedict(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items())+list(dict2.items()))
    return False

@app.route('/addcarts', methods=["POST"])
def add_cart():
    try:
        product_id = request.form.get("product_id")
        quantity = request.form.get("quantity")
        colors = request.form.get("colors")
        product = AddProduct.query.filter_by(id=product_id).first()
        if product_id and quantity and colors and request.method == "POST":
            DictItems = {product_id:
                             {'name': product.name,
                              'price': product.price,
                              'discount': product.discount,
                              'color': colors,
                              'quantity': quantity,
                              'image': product.image_1,
                              'colors': product.colors,}
                         }
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    print("This product is already in your cart")
                else:
                    session['Shoppingcart'] = mergedict(session['Shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = DictItems
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

@app.route('/carts')
def get_cart():
    if 'Shoppingcart' not in session:
        return redirect(request.referrer)
    for key, product in session['Shoppingcart'].items():
        discount = (product['discount']/100 * float(product['price']))
        subtotal = float(product['price']* int(product['quantity']))
        subtotal -= discount
        tax = ("%.2f") % (0.06 * float(subtotal))
        grandtotal = float("%.2f" % (1.06 * subtotal))
    return render_template('carts/carts.html', tax=tax, grandtotal=grandtotal)