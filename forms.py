from wtforms import Form, BooleanField, StringField, PasswordField, TextAreaField, IntegerField, validators
from flask_wtf.file import FileAllowed, FileField, FileRequired


class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


class LoginForm(Form):
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
    ])


class AddProductsForm(Form):
    name = StringField('Name', [validators.data_required()])
    price = IntegerField('Price', [validators.data_required()])
    discount = IntegerField('Discount', default=0)
    stock = IntegerField('Stock', default=0)
    description = TextAreaField("Description", [validators.data_required()])
    colors = TextAreaField("Colors", [validators.data_required()])
    image_1 = FileField("Image 1", validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    image_2 = FileField("Image 2", validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    image_3 = FileField("Image 3", validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])