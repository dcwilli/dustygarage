from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_login import login_required
from flask import session as login_session
from flask import session
from sqlalchemy import desc
from .models import User, Bid, Tool
from .forms import LoginForm, RegisterForm, CreateForm, SearchForm, LandingForm
import sqlalchemy as db
from . import db
import os
import re
from werkzeug.utils import secure_filename
from flask_table import Table, Col

bp = Blueprint("main", __name__)


@bp.route("/", methods=["GET", "POST"])
def index():
    tools = Tool.query.order_by(desc(Tool.date_created)).limit(4).all()
    print(tools)
    form_land = LandingForm()
    search_results = []
    search = SearchForm()
    if request.args.get("landing_search") != None:
        search_string = request.args.get("landing_search")
        print(search_string)
        all_tools = Tool.query.all()
        for tool in all_tools:
            if re.search(search_string, tool.tool_name, re.IGNORECASE):
                search_results.append(tool)
        return render_template("results.html", form=search, items=search_results)

    return render_template("index.html", form=form_land, tools=tools)


@bp.route("/manage")
@login_required
def manage():
    return render_template("manage.html")


# a simple function:does not handle errors in file types and file not being uploaded
def check_upload_file(form):
    # get file data from form
    fp = form.image.data
    filename = fp.filename
    # get the current path of the module file… store file relative to this path
    BASE_PATH = os.path.dirname(__file__)
    # upload file location – directory of this file/static/image
    upload_path = os.path.join(
        BASE_PATH, "static/img", secure_filename(filename))
    # store relative path in DB as image location in HTML is relative
    db_upload_path = "/static/img/" + secure_filename(filename)
    # save the file and return the db upload path
    fp.save(upload_path)

    return db_upload_path


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = CreateForm()
    print("search_results value is beneath")
    print(search_results)
    if form.validate_on_submit():
        print("Form validated")
        db_file_path = check_upload_file(form)
        new_tool = Tool(
            image=db_file_path,
            title=form.title.data,
            modelNo=form.modelNo.data,
            price=form.price.data,
            category=form.category.data,
            user_id=session.get("user_id"),
            description=form.description.data,
            brand=form.brand.data,
        )
        db.session.add(new_tool)

        db.session.commit()
        return redirect(url_for("main.create"))

    return render_template("create.html", form=form)


# use a for in the html to count the length of the string
@bp.route("/results", methods=["GET", "POST"])
def search():

    search = SearchForm()
    search_results = []

    if search.validate_on_submit():

        search_string = search.data["search"]
        if search_string != "":
            all_tools = Tool.query.all()
            print(all_tools[0].tool_name)
            for tool in all_tools:
                if re.search(search_string, tool.tool_name, re.IGNORECASE):
                search_results.append(tool)
        else:
            print("This string is empty")

        return render_template("results.html", form=search, items=search_results)

    return render_template("results.html", form=search)
