"""
Below model definition is for PostgreSQL.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, db.Identity(start=1, increment=1), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    mobile = db.Column(db.String(15), nullable=False, unique=True)
    email_id = db.Column(db.String(50), nullable=False, unique=False)

    def __init__(self, name, mobile, email_id):
        self.name = name
        self.mobile = mobile
        self.email_id = email_id


class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    menu_id = db.Column(db.Integer, db.Identity(start=1, increment=1), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    photo = db.Column(db.String(255), nullable=True)

    def __init__(self, name, category, price, photo=''):
        self.name = name
        self.category = category
        self.price = price
        self.photo = photo


class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, db.Identity(start=1, increment=1), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user_name = db.Column(db.String(50), nullable=False)
    order_placed_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship('User', backref=db.backref('orders', lazy=True))


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, db.Identity(start=1, increment=1), primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    description = db.Column(db.JSON, nullable=False)

    order = db.relationship('Order', backref=db.backref('order_items', lazy=True))

    def __init__(self, order_id, description):
        self.order_id = order_id
        self.description = description
