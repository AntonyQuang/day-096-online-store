from flask import render_template, session, request, url_for, flash, redirect
from admin.forms import RegistrationForm
from admin import app, db, bcrypt
from .models import User


@app.route('/')
def home():
    return render_template('/index.html', title="Admin Page")


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
        db.session.add(user)
        # db.session.commit()
        flash(f"Welcome {form.name.data}, thank you for registering", "success")
        return redirect(url_for('home'))
    return render_template('/register.html', form=form, title="Registration Page")
