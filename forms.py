from wtforms import Form, BooleanField, StringField, PasswordField, TextAreaField, IntegerField, validators, \
    DecimalField, SubmitField, ValidationError
from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask_wtf import FlaskForm
from models import Customer


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


class CustomerRegistrationForm(FlaskForm):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    country = StringField('Country', [validators.DataRequired()])
    state = StringField('State')
    city = StringField('City', [validators.DataRequired()])
    contact = StringField('Contact number')
    address_1 = StringField('Address 1', [validators.DataRequired()])
    address_2 = StringField('Address 2')
    zipcode = StringField('Zip Code', [validators.DataRequired()])

    profile_pic = FileField('Profile', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])

    submit = SubmitField('Register')

    def validate_username(self, username):
        if Customer.query.filter_by(username=username.data).first():
            raise ValidationError("This username is already in use!")

    def validate_email(self, email):
        if Customer.query.filter_by(email=email.data).first():
            raise ValidationError("This email address is already in use!")


class CustomerLoginForm(FlaskForm):
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired()])
