import datetime
from flask import (Blueprint, flash, render_template, session,
                   request, url_for, redirect)
from .models import Tool, Bid, User
from .forms import BidForm, MarkSold, UndoSold, CreateForm
from flask_login import login_user, login_required, logout_user
from werkzeug.utils import secure_filename
from decimal import Decimal, getcontext
import os
from . import db

bp = Blueprint('userdash', __name__, url_prefix='/userdash')


@bp.route('/main/<userid>', methods=["POST", "GET"])
@login_required
def maindash(userid):
    tool_length = session.get('tool_length', None)
    print(tool_length)
    return render_template('userdash/maindash.html', userid=userid, tool_length=tool_length)


@bp.route('/userselling/<userid>', methods=["POST", "GET"])
@login_required
def userselling(userid):

    print(userid)
    # query db for tools current user has listed
    tool = Tool.query.filter_by(user_id=userid).filter(
        Tool.sold_status == 0).all()
    tool_length = len(tool)
    session['tool_length'] = tool_length
    print(tool)
    print("-----------Tool length below----------------------")
    print(tool_length)
    return render_template('userdash/manageselling.html', userid=userid, tool=tool)


@bp.route('/userbids/<userid>', methods=["POST", "GET"])
@login_required
def userbids(userid):
    # query db for bids current user has made
    bids = db.session.query(Tool, Bid).join(
        Bid).filter_by(user_id=userid).all()
    print(bids)
    current_user = session.get('user_id')

    # if the url userid does not match the logged in user - log them out
    # if current_user != userid:
    #     return redirect(url_for('auth.logout'))
    return render_template('userdash/managebids.html', userid=userid, bids=bids)
