from . import db
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    bids = db.relationship("Bid", backref="user")

    def __repr__(self):
        return "<Name: {}, ID: {}>".format(self.name, self.id)


class Bid(db.Model):
    __tablename__ = "bids"
    id = db.Column(db.Integer, primary_key=True)
    bid_amount = db.Column(db.Float, nullable=False)
    bid_date = db.Column(db.DateTime, default=datetime.now())

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return "<Bid Amount: {}, ID: {}, user_id: {}>".format(
            self.bid_amount, self.id, self.user_id
        )


class Tool(db.Model):
    __tablename__ = "tools"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    modelNo = db.Column(db.String(100))
    price = db.Column(db.Float(100))
    category = db.Column(db.String(100))
    user_id = db.Column(db.Integer)
    description = db.Column(db.String(100))
    brand = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.now())
    sold = db.Column(db.String(100), default="No")

    def __repr__(self):
        return "<Bid Amount: {}, ID: {}, user_id: {}>".format(
            self.bid_amount, self.id, self.user_id
        )

