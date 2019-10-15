from flask import (Blueprint, flash, render_template, session,
                   request, url_for, redirect)
from .models import Tool, Bid, User
from .forms import ToolForm, BidForm, MarkSold, UndoSold, DeleteBid
from flask_login import login_user, login_required, logout_user
from werkzeug.utils import secure_filename
import os
from . import db

bp = Blueprint('tool', __name__, url_prefix='/tools')

# create a page that will show the details for the destination
@bp.route('/<id>', methods=["POST", "GET"])
def show(id):
    deleteForm = DeleteBid(request.form)
    user_obj = session.get('user_id')
    tool = Tool.query.filter_by(id=id).first()
    bid_user = Bid.query.filter_by(user_id=user_obj, tool_id=id).first()
    button_text = "Make a bid"
    current_bid_amount = ""
    print('current logged in user has the following bids for this item:')
    print(bid_user)
    print(tool)
    bform = BidForm()
    if bid_user is not None:
        current_bid_amount = bid_user.bid_amount
        # validate the delete bid form
    if request.method == "POST":
        bid_id = deleteForm.delete_bid.data
        print("BID ID:")
        print(bid_id)
        Bid.query.filter(id == bid_id).delete()
        db.session.commit()
        print('DELETED FROM DB')

    return render_template('tools/item.html', tool=tool, deleteForm=deleteForm, form=bform, button_text=button_text, bid_user=bid_user, current_bid_amount=current_bid_amount)


@bp.route('/<id>/manage', methods=["POST", "GET"])
def manage(id):
    soldForm = MarkSold(request.form)
    heading = "Not sure yet"
    undoForm = UndoSold(request.form)
    userid = session.get('user_id')
    tool = Tool.query.filter_by(id=id).first()
    sold_user = tool.soldStatus
    print('sold user ID&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    print(sold_user)
    bid_user = ""
    if sold_user == "":
        heading = "Printout of all unallocated bids"
        print(heading)
        bid_user = db.session.query(User, Bid).join(
            Bid).filter_by(tool_id=id).all()
        print('sold user is none$$$$$$$ / Bid User:')
        print(bid_user)
        print(tool)
    if sold_user != "":
        bid_user = db.session.query(User, Bid).filter(
            Bid.user_id == User.id).filter(Bid.tool_id == Tool.id).filter(Tool.soldStatus == Bid.id).all()
        print(" allocatted bids - should be sold")
        print(bid_user)

    if request.method == "POST":
        bid_userid = soldForm.bid_user_id.data
        print("bid_userid#######################")
        print(bid_userid)
        update_tool = Tool.query.get(id)
        print(update_tool)
        print("888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888888")
        update_tool.soldStatus = bid_userid

        # print(soldForm.userid.data)

        # db.session.add(sold_id)
        db.session.commit()
        print('COMMITED TO DB')
        print(tool)
        return redirect(url_for('tool.manage', id=id))

    return render_template('tools/manage.html', soldForm=soldForm, userid=userid, tool=tool, undoForm=undoForm, bid_user=bid_user)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = ToolForm()
    if form.validate_on_submit():
        print('Successfully validated form entries')

        db_file_path = check_file(form)

        # retrive form data and push to the db
        new_tool = Tool(tool_name=form.name.data,
                        brand=form.brand.data,
                        list_price=form.listingPrice.data,
                        images=db_file_path,
                        category=form.category.data,
                        desc=form.description.data,
                        userid=session.get('user_id'))

        # return redirect(url_for('tool.create'))
        db.session.add(new_tool)
        db.session.commit()
        print('COMMITED TO DB')
        flash('Tool successfully created')
        return redirect(url_for('tool.create'))
    return render_template('tools/create.html', form=form)


@bp.route('/<toolid>/bid', methods=['GET', 'POST'])
def bid(toolid):
    form = BidForm()

    user_obj = session.get('user_id')
    # check if a bid exists for this user
    bid_user = Bid.query.filter_by(user_id=user_obj, tool_id=toolid).first()

    if bid_user is None:
        # get the tool object associated with the page
        if form.validate_on_submit():
            bid = Bid(bid_amount=form.bidamount.data,
                      tool_id=toolid, user_id=user_obj)
            # add and commit to bid db
            db.session.add(bid)
            db.session.commit()
            print('Your bid has been added', 'success')
            # flash('Bid successfully sent to seller')
    else:
        if form.validate_on_submit():
            bid_id = bid_user.id
            bid = form.bidamount.data
            print(bid)
            # retrieve current bid
            current_bid = Bid.query.get(bid_id)
            print(current_bid)
            current_bid.bid_amount = bid

            db.session.commit()
            print('Your bid has been updated', 'success')

    # redirect to the item page
    return redirect(url_for('tool.show', id=toolid))


def check_file(form):
    fp = form.files.data

    # retrieve the file
    filename = fp.filename
    print(fp.filename)
    # Current OS path of the file
    BASE_PATH = os.path.dirname(__file__)

    upload_path = os.path.join(
        BASE_PATH, 'static/img', secure_filename(filename))
    db_upload_path = secure_filename(filename)
    print(db_upload_path)
    fp.save(upload_path)
    return db_upload_path
