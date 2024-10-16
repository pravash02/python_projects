import logging
import os
from collections import defaultdict
from datetime import timedelta, datetime

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_session import Session
from cafe_web.libs.query_result_handler import get_menu_data, get_cart_data
from cafe_web.libs.send_otp import OTPClass
from cafe_web.libs.models import db, User, MenuItem, OrderItem, Order, CartItem

os.urandom(24)

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY', 'fallback_secret_key')

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'postgresql://pravashpanigrahi:prav%400411@localhost/prav'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_SQLALCHEMY'] = db
app.config['SESSION_PERMANENT'] = False

db.init_app(app)
app.config['SESSION_SQLALCHEMY'] = db

Session(app)


logger = logging.getLogger(__name__)

carts = {}


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user_mobile'] = request.form['mobile']

        # query the Database with the mobile no to get the user details
        user = User.query.filter_by(mobile=session['user_mobile']).first()
        if user:
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['email_id'] = user.email_id

            # clear the existing cart for the user when they log in
            CartItem.query.filter_by(user_id=user.id).delete()
            db.session.commit()

            flash(f"Hi {session['user_name']}, Welcome back. Please select menu to order")
            return redirect(url_for('menu'))

        else:
            flash(f"Please enter below details")
            return render_template('register_user.html')

    return render_template('login.html')


@app.route('/register-user', methods=['GET', 'POST'])
def register_user():
    if 'user_mobile' not in session:
        flash("Please enter your mobile no first")
        return redirect(url_for('login'))

    if request.method == 'POST':
        session['user_name'] = request.form.get('user_name')
        session['email_id'] = request.form.get('email_id')

        # TODO: Logic for sending otp to user's mobile no

        # sending otp to user's email id
        otp_obj = OTPClass(session['email_id'], session['user_name'])
        otp = otp_obj()
        session['otp'] = otp

        flash(f"OTP has been sent to {session['user_mobile']} / {session['email_id']}. Please enter the OTP to proceed.")
        return redirect(url_for('otp_validation'))

    return render_template('register_user.html')


@app.route('/otp-validation', methods=['GET', 'POST'])
def otp_validation():
    if 'user_mobile' not in session:
        flash("Please enter your mobile no first")
        return redirect(url_for('login'))

    if request.method == 'POST':
        entered_otp = (
                request.form.get('otp-1', '') +
                request.form.get('otp-2', '') +
                request.form.get('otp-3', '') +
                request.form.get('otp-4', '')
        )

        if entered_otp == session['otp']:
            # insert user's info to Users table
            new_user = User(name=session['user_name'], mobile=session['user_mobile'], email_id=session['email_id'])
            db.session.add(new_user)
            db.session.commit()

            session['user_id'] = new_user.id

            flash("OTP validated successfully!")
            flash(f"Hi {session['user_name']}, Welcome!, You have been registered successfully.")
            return redirect(url_for('menu'))

        else:
            flash("Invalid OTP. Please try again")
            return render_template('otp_validation.html')

    return render_template('otp_validation.html')


@app.route('/menu', methods=['GET', 'POST'])
def menu():
    # Get the menu from the database
    menu_query_result = MenuItem.query.all()
    menu_items = get_menu_data(menu_query_result)

    if 'user_id' not in session:
        flash("Please log in to continue")
        return redirect(url_for('login'))

    if request.method == 'POST':
        if session['user_mobile'] not in carts:
            carts[session['user_mobile']] = []

        selected_items = False

        # Iterate over menu items and process the form data
        for item in menu_query_result:
            quantity_key = f"quantity_{item.menu_id}"
            quantity = int(request.form.get(quantity_key, 0))

            if quantity > 0:
                selected_items = True
                # Check if item is already in cart
                existing_cart_item = CartItem.query.filter_by(user_id=session['user_id'], menu_item_id=item.menu_id).first()
                if existing_cart_item:
                    existing_cart_item.quantity += quantity
                else:
                    # Add new item to cart
                    new_cart_item = CartItem(user_id=session['user_id'], menu_item_id=item.menu_id, quantity=quantity)
                    db.session.add(new_cart_item)

        if selected_items:
            db.session.commit()
            flash("Selected items have been added to the cart.")
        else:
            flash("Please select at least one item to add to the cart.")

    user_cart_items = CartItem.query.filter_by(user_id=session['user_id']).all()
    has_cart_items = len(user_cart_items) > 0

    return render_template('menu.html', menu_items=menu_items, has_cart_items=has_cart_items)


@app.route('/cart', methods=['GET', 'POST'])
def cart_view():
    description = defaultdict(int)

    if 'user_id' not in session:
        flash("Please log in to continue")
        return redirect(url_for('login'))

    cart_query_result = CartItem.query.filter_by(user_id=session['user_id']).all()
    cart_items = get_cart_data(cart_query_result)

    total_price = sum(item.menu_item.price * item.quantity for item in cart_query_result)
    total_quantity = sum(item.quantity for item in cart_query_result)

    if request.method == 'POST':
        # insert order details to Orders table
        new_order = Order(user_id=session['user_id'], user_name=session['user_name'], order_placed_date=datetime.now())
        db.session.add(new_order)
        db.session.commit()

        session['order_id'] = new_order.order_id

        for cart_item in cart_query_result:
            description[cart_item.menu_item.name] += cart_item.quantity

        # insert a single row into the OrderItem table with the combined description
        order_item = OrderItem(
            order_id=new_order.order_id,
            description=dict(description)  # Convert defaultdict to a standard dict
        )
        db.session.add(order_item)
        db.session.commit()

        return redirect(url_for('order_success'))

    return render_template('cart.html', cart=cart_query_result, total_price=total_price, total_quantity=total_quantity)


@app.route('/order-success')
def order_success():
    carts.pop(session['user_mobile'], None)
    order_number = session['order_id']
    session.clear()
    return render_template('success.html', order_number=order_number)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Tables checked and created (if not existing).")

    app.run(debug=True)
