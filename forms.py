from wtforms import Form, BooleanField, StringField, PasswordField, TextAreaField, IntegerField, validators, DecimalField, SubmitField
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
    price = DecimalField('Price', [validators.data_required()], places=2, rounding=None)
    discount = IntegerField('Discount', default=0)
    stock = IntegerField('Stock', default=0)
    description = TextAreaField("Description", [validators.data_required()])
    colors = TextAreaField("Colors", [validators.data_required()])
    image_1 = FileField("Image 1", validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    image_2 = FileField("Image 2", validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    image_3 = FileField("Image 3", validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])


class CustomerRegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    country = StringField('Country', [validators.data_required()])
    state = StringField('State')
    city = StringField('City', [validators.data_required()])
    contact = StringField('Contact number', [validators.data_required()])
    address_1 = StringField('Address 1', [validators.data_required()])
    address_2 = StringField('Address 2')
    zipcode = StringField('Zip Code', [validators.data_required()])

    profile_pic = FileField('Profile', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])

    submit = SubmitField('Register')