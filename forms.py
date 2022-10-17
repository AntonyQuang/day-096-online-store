from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, URL, Length


##WTForm

class CreateItemForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    description = StringField("Item Description", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


class RegisterForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    address_1 = StringField("Address 1",  validators=[DataRequired()])
    address_2 = StringField("Address 2")
    city = StringField("City", validators=[DataRequired()])
    postcode = StringField("Post Code",  validators=[DataRequired(), Length(min=4, max=10)])
    country = StringField("Country", validators=[DataRequired()])
    submit = SubmitField("Sign me up!")


class LogInForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let me in!")

