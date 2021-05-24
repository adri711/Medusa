from flask_sqlalchemy import SQLAlchemy
from src import db
from datetime import datetime

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(62), unique=False, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	first_name = db.Column(db.String(42), nullable=False)
	last_name = db.Column(db.String(42), nullable=False)
	biography = db.Column(db.String(250))
	profile_pic = db.Column(db.String(52))
	buyer_xp = db.Column(db.Integer, nullable=False)
	seller_xp = db.Column(db.Integer, nullable=False)
	permission = db.Column(db.Integer, nullable=False) # Admin permission
	password = db.Column(db.String(320), nullable=False)
	date_registered = db.Column(db.DateTime, default=datetime.now)
	product_owner = db.relationship("Product", backref="author", lazy=True)
	purchase_owner = db.relationship("Purchase", backref="author", lazy=True)
	purchase_owner = db.relationship("Cart", backref="owner", lazy=True)

	def __repr__(self):
		return f"User({self.username} #{self.tag}, {self.email}, {self.first_name} {self.last_name})"

class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(42), nullable=False)
	price = db.Column(db.Float, nullable=False)
	product_type = db.Column(db.String(6), nullable=False)
	product_image = db.Column(db.String(52), nullable=False)
	owned_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	purchased_item = db.relationship("items_sold", backref="author", lazy=True)
	purchased_item = db.relationship("Cart", backref="product", lazy=True)
	def __repr__(self):
		return f"Product {self.id}, {self.name}, {self.price}"

class Cart(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	item_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False) # product id
	amount = db.Column(db.Integer, nullable=False)
	size = db.Column(db.String(5), nullable=False)
	color = db.Column(db.String(12), nullable=False)

class Purchase(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	purchased_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	date = db.Column(db.DateTime, default=datetime.now)
	cost = db.Column(db.Float, nullable=False)
	state = db.Column(db.String(32), nullable=False)
	money_received = db.Column(db.Float)
	item = db.relationship("items_sold", backref="purchase_group", lazy=True)
	def __repr__(self):
		return f"Purchase #{self.id}, on {self.date} by {User.query.filter_by(id=self.purchased_by).first().username}"

class items_sold(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
	purchase_id = db.Column(db.Integer, db.ForeignKey('purchase.id'), nullable=False)
	price_paid = db.Column(db.Float, nullable=False)
	amount = db.Column(db.Integer, nullable=False)
	size = db.Column(db.String(5), nullable=False)
	color = db.Column(db.String(12), nullable=False)
	def __repr__(self):
		return f"items_sold: #{id} ..."