from . import db
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, nullable=False)
    lastName = db.Column(db.String(100), index=True, nullable=False)
    emailid = db.Column(db.String(100), index=True,
                        unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    bids = db.relationship('Bid', backref='user')
    tools = db.relationship('Tool', backref='user')

    def __repr__(self):
        return "<Name: {}, ID: {}>".format(self.name, self.id)


class Bid(db.Model):
    __tablename__ = 'bids'
    id = db.Column(db.Integer, primary_key=True)
    bid_amount = db.Column(db.Float, nullable=False)
    bid_date = db.Column(db.DateTime, default=datetime.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tool_id = db.Column(db.Integer, db.ForeignKey('tools.id'))

    def __repr__(self):
        return "<bid_amount: {}, id: {}, user_id: {}, tool_id: {}>".format(self.bid_amount, self.id, self.user_id, self.tool_id)


class Tool(db.Model):
    __tablename__ = "tools"
    id = db.Column(db.Integer, primary_key=True)
    tool_name = db.Column(db.String(100))
    modelNo = db.Column(db.String(100))
    list_price = db.Column(db.Float(100))
    images = db.Column(db.String(1000), default='noimage.png')
    category = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    desc = db.Column(db.String(100))
    brand = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=datetime.now())
    sold_status = db.Column(db.String(100), default="No")

    bid_id = db.relationship('Bid', backref='tools')

    def __repr__(self):
        return "<Tool Name: {}, Tool ID: {}, Brand: {}, sold_status: {}>".format(
            self.tool_name, self.id, self.brand, self.sold_status
        )
