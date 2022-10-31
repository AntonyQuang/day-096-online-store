from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Creating a Flask instance
app = Flask(__name__)
app.config["SECRET_KEY"] = "SecretKey"
# Connect to the database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shop.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

