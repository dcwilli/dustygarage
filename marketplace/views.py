from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_login import login_required
from flask import session as login_session
from flask import session
from .models import User, Bid, Tool
from .forms import LoginForm, RegisterForm, CreateForm, SearchForm, Results, LandingForm
import sqlalchemy as db
from . import db

import re
from flask_table import Table, Col

print("this is __name__")
print(type(__name__))
print(__name__)

bp = Blueprint("main", __name__)


@bp.route("/", methods=["GET", "POST"])
def index():
    print()
    form_land = LandingForm()
    print("Form has not validated")
    search_results = []
    search = SearchForm()
    if request.args.get("landing_search") != None:
        print("Form has validated")
        search_string = request.args.get("landing_search")
        print(search_string)

        all_tools = Tool.query.all()
        for tool in all_tools:
            if re.search(search_string, tool.title):
                search_results.append(tool)

        print("Below is Search results")

        # display results
        table = Results(search_results)
        table.border = True
        # del input_string
        return render_template("results.html", form=search, table=table)
    return render_template("index.html", form=form_land)


@bp.route("/manage")
@login_required
def manage():
    return render_template("manage.html")


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = CreateForm()

    if form.validate_on_submit():
        print("Form validated")
        new_tool = Tool(
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


@bp.route("/results", methods=["GET", "POST"])
def search():

    search = SearchForm()
    search_results = []

    if search.validate_on_submit():

        search_string = search.data["search"]
        print(search_string)
        if search_string != "":
            all_tools = Tool.query.all()
            for tool in all_tools:
                if re.search(search_string, tool.title):
                    search_results.append(tool)
        else:
            print("This string is empty")
        print("Below is Search results")

        # display results
        table = Results(search_results)
        table.border = True
        return render_template("results.html", form=search, table=table)

    return render_template("results.html", form=search)
