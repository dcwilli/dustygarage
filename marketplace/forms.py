from flask_wtf import FlaskForm
from flask_table import Table, Col, BoolCol, DateCol
from wtforms.fields import (
    TextAreaField,
    SubmitField,
    StringField,
    PasswordField,
    SelectField,
)
from wtforms.validators import InputRequired, Length, Email, EqualTo


# creates the login information
class LoginForm(FlaskForm):
    username = StringField("User Name", validators=[
                           InputRequired("Enter user name")])
    password = PasswordField(
        "Password", validators=[InputRequired("Enter user password")]
    )
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    username = StringField("User Name", validators=[InputRequired()])
    email = StringField(
        "Email Address", validators=[Email("Please enter a valid email")]
    )

    # linking two fields - password should be equal to data entered in confirm
    password = PasswordField(
        "Password",
        validators=[
            InputRequired(),
            EqualTo("confirm", message="Passwords should match"),
        ],
    )
    confirm = PasswordField("Confirm Password")
    # submit button
    submit = SubmitField("Register")


class CreateForm(FlaskForm):

    title = StringField("Title", validators=[InputRequired()])
    modelNo = StringField("Model Number", validators=[InputRequired()])
    price = StringField("Price", validators=[InputRequired()])
    category = SelectField(
        u"Category",
        choices=[
            ("Gardening", "Gardening"),
            ("Garage Tools", "Garage Tools"),
            ("Renovation Tools", "Renovation Tools"),
            ("Industrial Tools", "Industrial Tools"),
            ("Other Tools", "Other Tools"),
        ],
    )
    description = StringField("Description", validators=[InputRequired()])
    brand = StringField("Brand", validators=[InputRequired()])
    submit = SubmitField("Create")


class SearchForm(FlaskForm):
    search = StringField("")
    search_button = SubmitField("Search")


class LandingForm(FlaskForm):
    landing_search = StringField("", validators=[InputRequired()])
    landing_search_button = SubmitField("Search")


class Results(Table):
    title = Col("title")
    modelNo = Col("modelNo")
    price = Col("price")
    category = Col("category")
    description = Col("description")
    brand = Col("brand")
    date = DateCol("date")
    sold = Col("sold")
