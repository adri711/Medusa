from flask import Flask, app, render_template, url_for, flash, redirect, request, jsonify, g, session
from src import application, bcrypt,db, constants
from src.forms import LoginForm, RegisterForm, BillingForm
from src.models import User, Product, Cart,Purchase, items_sold
from src.utils import is_user_logged,get_user_id,get_user_level
from werkzeug.utils import secure_filename
import os, requests,json

@application.before_request
def get_user_info():
	g.user = None
	if 'user_id' in session:
		g.user = User.query.filter_by(id=session['user_id']).first()

@application.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")

@application.route("/test")
def add_product():
    counter = "item " + str(Product.query.filter_by(product_type=constants.SHIRTS).count())
    db.session.add(Product(name=counter, product_type=constants.SHIRTS, price=25, product_image="/uploads/m1.png", owned_by=1))
    db.session.commit()
    return "Added product"

@application.route("/store/<string:product>/", methods=["POST", "GET"])
@application.route("/store/<string:product>/<int:page>", methods=["POST", "GET"])
def store(product, page=1):
    if request.method == 'GET':
        username = ''
        if g.user:
            username=g.user.username
        return render_template("main.html", title='Store', username=username, user_id=get_user_id(), user_logged=is_user_logged(), product=product, page=page,pages_count=Product.query.filter_by(product_type=product).count() // constants.ITEMS_PER_PAGE + 1)
    # else if the method is post...
    session['last_visit'] = product
    if product == constants.SHIRTS:
        products = Product.query.filter(Product.product_type==constants.SHIRTS, Product.id >= (page-1)*constants.ITEMS_PER_PAGE).limit(constants.ITEMS_PER_PAGE).all()
        return render_template("products_display.html", products=[{'design':product, 'user': User.query.filter_by(id=product.owned_by).first()} for product in products])
    
    elif product == constants.JEWELRY:
        products = Product.query.filter(Product.product_type==constants.JEWELRY, Product.id >= (page-1)*constants.ITEMS_PER_PAGE).limit(constants.ITEMS_PER_PAGE).all()
        return render_template("products_display.html", products=[{'design':product, 'user': User.query.filter_by(id=product.owned_by).first()} for product in products])
    # else 
    return render_template("404.html")

@application.route("/login", methods=["POST", "GET"])
@application.route("/signin", methods=["POST", "GET"])
def signin():
    next_page = request.args.get('next')
    k = request.referrer
    if g.user:
        return redirect(next_page) if next_page else redirect(url_for('store', product=session['last_visit']))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            return redirect(next_page) if next_page else redirect(request.referrer)
        else:
            flash("The details you've enterred are incorrect, please double check.")
    return render_template("login.html", title="Login", form=form)


@application.route("/register", methods=["POST", "GET"])
@application.route("/signup", methods=["POST", "GET"])
def signup():
    if g.user:
        return redirect(url_for('store', product=session['last_visit'])) if session['last_visit'] else redirect(url_for("index"))
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if request.files['avatar']:
            filename = str(User.query.count())
            request.files['avatar'].save(os.path.join(application.config['FILE_UPLOADS'], filename))
            filename = f"images/uploads/users_avatars/{filename}"
        else:
            filename = 'images/uploads/users_avatars/default_avatar.jpg'
        new_user = User(first_name=form.first_name.data, last_name=form.last_name.data,
            username=form.username.data,email=form.email.data, password=password, profile_pic=filename, buyer_xp=0, seller_xp=0, permission=0)
        db.session.add(new_user)
        db.session.commit()
        flash("Successfuly registered. You can log into your account now.")
        return redirect(url_for('signin'))
    return render_template("register.html", title="Register", form=form)

@application.route("/logout/", methods=["POST", "GET"])
@application.route("/signout/", methods=["POST", "GET"])
def logout():
    if 'user_id' in session:
        session.pop('user_id')
    print(request.referrer)
    return redirect(request.referrer) if request.referrer else redirect(url_for('index'))

@application.route("/user/<int:id>", methods=["POST", "GET"])
@application.route("/user/<int:id>/<int:page_id>", methods=["POST", "GET"])
def user(id,page_id=1):
    if request.method == 'GET':
        user = User.query.filter_by(id=id).first()
        buy_level = get_user_level(g.user.buyer_xp)
        sell_level = get_user_level(g.user.seller_xp)
        return render_template("profile.html",  username=user.username, title="Profile", page=page_id, user_id=get_user_id(), levels={'buy': buy_level, 'sell':sell_level}, user_logged=is_user_logged(), pages_count=Product.query.filter_by(owned_by=id).count() // constants.ITEMS_PER_PAGE + 1, \
                    user_profile={'userid': id, 'username': user.username, 'firstname': user.first_name, 'lastname': user.last_name, 'avatar': user.profile_pic, 'biography':user.biography})
    # else
    user_products = Product.query.filter(Product.owned_by==id, 
            Product.id >= Product.query.count() - (page_id * (constants.ITEMS_PER_PAGE+1))) \
            .limit(constants.ITEMS_PER_PAGE).all()
    return render_template("products_display.html",products=reversed([{'design': user_product, 'user': User.query.filter_by(id=id).first()} for user_product in user_products])) if user_products else "<div style='position:relative; left: 25px;'>This user doesn't have any designs</div>"

@application.route("/cart")
def cart():
    if g.user:
        total_price, items = 0, [ {
                'order_details': item, 
                'product_details': Product.query.filter_by(id=item.item_id).first()
            }
            for item in Cart.query.filter_by(user_id=g.user.id).all()
        ]
        for item in items: total_price = total_price + item['product_details'].price * item['order_details'].amount
        return render_template("cart.html", title="Cart", items=items, total_price=total_price,user_id=get_user_id(),user_logged=is_user_logged())
    return redirect(url_for("signin"))

@application.route("/add-to-cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    color = request.form['color']
    size = request.form['size']
    if  'user_id' in session:
        db.session.add(Cart(user_id=g.user.id, item_id=product_id, amount=1, size=size, color=color))
        db.session.commit()
    return jsonify({"state": 'user_id' in session})

@application.route("/alter-item-order", methods=["POST"])
def alter_item_order():
    if not g.user:
        return
    cart_order_id, new_size,new_color,new_quantity = request.form['id'], request.form['size'], request.form['color'], request.form['quantity']
    row = Cart.query.filter_by(id=cart_order_id).first()
    if row.user_id == session['user_id']:
        row.amount = new_quantity
        row.color = new_color
        row.size = new_size
        db.session.commit()
        return jsonify({"status": "SUCCESS"})
    return jsonify({'status': 'FAIL', 'message': "You're trying to access someone else's cart."})

@application.route('/delete-item-order', methods=['POST'])
def delete_item_order():
    if not g.user:
        return
    item_order = request.form['id']
    item_target = Cart.query.filter_by(id=item_order).first()
    if item_target.user_id == session['user_id']:
        Cart.query.filter_by(id=item_order).delete()
        db.session.commit()
        return jsonify({"status": "SUCCESS"})
    return jsonify({'status': 'FAIL', 'message': "You're trying to access someone else's cart."})

@application.route("/billing", methods=["GET", "POST"])
def billing():
    form = BillingForm(request.form)
    if g.user:
        items = [
            {
            'order_details': {
                'id': item.id,
                'item_id':item.item_id,
                'amount': item.amount,
                'color': item.color,
                'size': item.size
            },
            'product_details': {
                'name': Product.query.filter_by(id=item.item_id).first().name,
                'price': Product.query.filter_by(id=item.item_id).first().price
                } 
            } 
            for item in Cart.query.filter_by(user_id=session['user_id']).all()
        ]
        if form.validate_on_submit():
            session['current_billing'] = {
                'first_name': form.first_name.data if form.first_name.data else User.query.filter_by(id=session['user_id']).first().first_name,
                'last_name': form.last_name.data if form.last_name.data else User.query.filter_by(id=session['user_id']).first().last_name,
                'city': form.city.data,
                'address': form.address.data,
                'phone': form.phone.data,
                'phone2': form.phone2.data
            }
            return redirect(url_for('checkout'))
        total_price = 0
        for item in items: total_price = total_price + item['product_details']['price'] * item['order_details']['amount']
        session['orders_on_check'] = items
        return render_template("billing.html", title="Billing", total=total_price,enable=False, form=form,user_logged=is_user_logged(), user_id=session['user_id'],items=items)
    return redirect(request.referrer if request.referrer else 'index')

@application.route("/checkout", methods=["GET", "POST"])
def checkout():
    if g.user:
        total_price = 0
        for item in session['orders_on_check']: total_price = total_price + item['product_details']['price'] * item['order_details']['amount']
        return render_template("checkout.html", title="checkout",user_info=session['current_billing'], total=total_price, items=session['orders_on_check'], user_logged=is_user_logged(), user_id=session['user_id'])
    return "404 Not found"

@application.route('/payment', methods=['GET','POST'])
def handle_data():
    if 'payment_id' in request.form and 'flouci_otp' in request.form and g.user and 'orders_on_check' in session:
        paymentid = request.form['payment_id']
        flouciotp = request.form['flouci_otp']
        total_price = 0
        for item in session['orders_on_check']: total_price = total_price + item['product_details']['price'] * item['order_details']['amount']
        r = requests.post('https://developers.flouci.com/api/accept', json={
            'app_token': paymentid, 
            'app_secret': application.config['flouci_private'], 
            'app_public': application.config['flouci_public'], 
            'payment_id': paymentid,
            'amount': total_price,
            'flouci_otp': flouciotp
        })
        response = json.loads(r.text)
        if response['result']['status'] == 'SUCCESS':
            purchase = Purchase(purchased_by=g.user.id, cost=total_price, money_received=response['result']['amount'], state="En cours de traitement.")
            db.session.add(purchase)
            db.session.flush()
            for item_order in session['orders_on_check']:
                Cart.query.filter_by(id=item_order['order_details']['id']).delete()
                User.query.filter_by(id=Product.query.filter_by(id=item_order['order_details']['item_id']).first().owned_by).first().seller_xp +=100
                User.query.filter_by(id=g.user.id).first().buyer_xp+=100
                db.session.add(items_sold(
                        product_id=item_order['order_details']['item_id'], 
                        purchase_id=purchase.id, 
                        amount=item_order['order_details']['amount'], 
                        size=item_order['order_details']['size'],
                        color=item_order['order_details']['color'],
                        price_paid=item_order['order_details']['amount']*item_order['product_details']['price']
                    )
                )
            db.session.commit()
            session['orders_on_check'] = None
            session['billing'] = None
        return redirect(url_for('orders'))
    return "We've encountered an error with your request."

@application.route("/orders", methods=['POST', 'GET'])
def orders():
    if g.user:
        return render_template("orders.html", title="Orders", user_id=get_user_id(), user_logged=is_user_logged(),purchases=Purchase.query.filter_by(purchased_by=g.user.id).all())
    else:
        return redirect(url_for("index"))