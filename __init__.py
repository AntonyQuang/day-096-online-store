from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads
import os

basedir = os.path.abspath(os.path.dirname(__file__))
# Creating a Flask instance
app = Flask(__name__)
app.config["SECRET_KEY"] = "SecretKey"
# Connect to the database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shop.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, "static/images")
# Adding image upload onto app
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

