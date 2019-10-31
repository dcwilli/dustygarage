from flask_wtf import FlaskForm
from flask_table import Table, Col, BoolCol, DateCol
from wtforms.fields import (
    TextAreaField,
    SubmitField,
    StringField,
    PasswordField,
    SelectField,
    HiddenField
)
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed, FileRequired


# creates the login information
class LoginForm(FlaskForm):
    emailid = StringField("Email Address", validators=[
        InputRequired('Enter email address')])
    password = PasswordField("Password", validators=[
                             InputRequired('Enter user password')])
    submit = SubmitField("Login")

# Register User


class RegisterForm(FlaskForm):
    name = StringField("First Name", validators=[InputRequired()])
    lastName = StringField("Last Name", validators=[InputRequired()])
    email = StringField("Email Address", validators=[
                        Email("Please enter a valid email")])

    # linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(),
                                                     EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    # submit button
    submit = SubmitField("Register")


ALLOWED_FILE = {'png', 'jpg', 'JPG', 'PNG', 'bmp'}

# List item


class CreateForm(FlaskForm):

    tool_name = StringField("Title", validators=[InputRequired()])

    list_price = StringField("Price", validators=[InputRequired()])
    category = SelectField(
        u"Category",
        choices=[
            ("Garden", "Garden"),
            ("General Hardware",  "General Hardware"),
            ("Building and Hardware", "Building and Hardware"),
            ("Hand Tools", "Hand Tools"),
            ("Power Tools", "Power Tools"),
        ],
    )
    desc = TextAreaField("Description", validators=[InputRequired()])
    brand = StringField("Brand", validators=[InputRequired()])
    images = FileField("Select an Image  ", validators=[FileRequired(message="Image can not be empty"),
                                                        FileAllowed(ALLOWED_FILE, message="Only support jpg, JPG, png, bmp")])
    submit = SubmitField("Create")

# search page form


class SearchForm(FlaskForm):
    search = StringField("")
    search_button = SubmitField("Search")

# landing page form


class LandingForm(FlaskForm):
    landing_search = StringField("", validators=[InputRequired()])
    landing_search_button = SubmitField("Search")

# Results table for search


class Results(Table):
    tool_name = Col("title")
    modelNo = Col("modelNo")
    list_price = Col("price")
    category = Col("category")
    desc = Col("description")
    brand = Col("brand")
    date_created = DateCol("date")
    sold_status = Col("sold")

# Marking item as sold in manage item


class MarkSold(FlaskForm):
    bid_user_id = HiddenField('bid_user id', '{{user.user_id}}')
    submit = SubmitField("Mark as Sold")

# Undo item as sold in manage item


class UndoSold(FlaskForm):
    undoSold = HiddenField("zero")
    submit_undo = SubmitField("Undo")

# Bidding on an item in item page


class BidForm(FlaskForm):
    bidamount = StringField("Bid Amount", validators=[InputRequired()])
    submit = SubmitField("Submit Bid")
