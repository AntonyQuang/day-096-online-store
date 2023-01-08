from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads
import os
from flask_msearch import Search
from flask_login import LoginManager

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
search = Search()
search.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'customer_login'
login_manager.needs_refresh_message_category="danger"
login_manager.login_message = u"Please login first"