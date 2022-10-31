from flask import render_template

from admin import app


@app.route('/')
def home():
    return "Home page of your shop"


@app.route('/register')
def register():
    return render_template('/register.html', title="Register user")
