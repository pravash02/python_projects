import logging
import os
import random
from datetime import timedelta

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_session import Session
from cafe_web.libs.connection import DBConnection
from cafe_web.libs.send_otp import OTPClass
from cafe_web.libs.models import db, User
from flask_wtf.csrf import CSRFProtect

os.urandom(24)

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY', 'fallback_secret_key')

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'postgresql://pravashpanigrahi:prav%400411@localhost/prav'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_SQLALCHEMY'] = db
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True

db.init_app(app)
app.config['SESSION_SQLALCHEMY'] = db

# csrf = CSRFProtect(app)
Session(app)


logger = logging.getLogger(__name__)

carts = {}

# Mock Data for Users
users = [
    {'id': 1, 'name': 'pravash', 'mobile': 7875753393, 'email_id': "pravash.cse@gmail.com"},
    {'id': 2, 'name': 'shelley', 'mobile': 8637292526, 'email_id': "shelley.tripathy@gmail.com"},
]
# Mock Data for Food and Drinks
menu_items = [
    {'menu_id': 1, 'name': 'Cappuccino', 'category': 'Coffee', 'price': 5, 'photo': ''},
    {'menu_id': 2, 'name': 'Latte', 'category': 'Coffee', 'price': 4, 'photo': ''},
    {'menu_id': 3, 'name': 'Mocha', 'category': 'Coffee', 'price': 6, 'photo': ''},
    {'menu_id': 4, 'name': 'Hazelnut', 'category': 'Flavoured Coffee', 'price': 4.5, 'photo': ''},
    {'menu_id': 5, 'name': 'Caramel', 'category': 'Flavoured Coffee', 'price': 4.5, 'photo': ''},
    {'menu_id': 6, 'name': 'Mocha', 'category': 'Flavoured Coffee', 'price': 3.5, 'photo': ''},
    {'menu_id': 7, 'name': 'Cinnamon', 'category': 'Flavoured Coffee', 'price': 4, 'photo': ''},
    {'menu_id': 8, 'name': 'Peppermint', 'category': 'Flavoured Coffee', 'price': 3.5, 'photo': ''},
    {'menu_id': 9, 'name': 'Chocolate Brownie', 'category': 'Pastry', 'price': 3, 'photo': ''},
    {'menu_id': 10, 'name': 'Caramel shortbread', 'category': 'Pastry', 'price': 5, 'photo': ''},
    {'menu_id': 11, 'name': 'Chocolate Truffle', 'category': 'Pastry', 'price': 2.8, 'photo': ''},
    {'menu_id': 12, 'name': 'Croissant', 'category': 'Pastry', 'price': 3.5, 'photo': ''},
    {'menu_id': 13, 'name': 'Chocolate Cookies', 'category': 'Pastry', 'price': 3.1, 'photo': ''},
    {'menu_id': 14, 'name': 'Honey & Raisin Cake', 'category': 'Pastry', 'price': 3, 'photo': ''},
    {'menu_id': 15, 'name': 'Muffins', 'category': 'Pastry', 'price': 2.4, 'photo': ''},
]


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mobile = request.form['mobile']

        # TODO: Logic to query the Database with the mobile no
        # user = User.query.filter_by(mobile=mobile).first()
        # if user:
        #     session['user_id'] = user.id
        #     session['user_name'] = user.username
        #     session['user_mobile'] = user.mobile
        #     session['user_mobile'] = user.email_id

        # TODO: for testing
        user = users[0]
        if str(user['mobile']) == mobile:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_mobile'] = user['mobile']
            session['user_email'] = user['email_id']

            flash(f"Hi {user['name']}, Welcome back. Please select menu to order")
            return redirect(url_for('menu'))

        else:
            session['user_mobile'] = mobile

            flash(f"Please enter below details")
            return render_template('register_user.html')

    return render_template('login.html')


@app.route('/register-user', methods=['GET', 'POST'])
def register_user():
    if 'user_mobile' not in session:
        flash("Please enter your mobile no first")
        return redirect(url_for('login'))

    if request.method == 'POST':
        user_name = request.form.get('user_name')
        email_id = request.form.get('email_id')

        # TODO: Logic to insert user's info to Users table
        # conn = get_db_connection()
        # conn.execute('INSERT INTO users (user_name, mobile_no, email_id) VALUES (?, ?)',
        #              (user_name, session['mobile'], email_id))
        # conn.commit()

        # TODO: Logic to retrieve user's info
        # user = conn.execute("")
        # if user:
        #     session['user_name'] = user_name
        #     session['user_id'] = user.id
        #     session['email_id'] = user.email_id
        # conn.close()

        # TODO: To be removed
        user = users[0]
        session['user_name'] = user_name
        session['user_id'] = user['id']
        session['user_email_id'] = email_id

        # TODO: Logic for sending otp to user's mobile no

        # sending otp to user's email id
        otp_obj = OTPClass(email_id, user_name)
        otp = otp_obj()
        session['otp'] = otp

        flash(f"OTP has been sent to {session['user_mobile']} / {email_id}. Please enter the OTP to proceed.")
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
            flash("OTP validated successfully!")
            flash(f"Hi {session['user_name']}, Welcome!, You have been registered successfully.")
            return redirect(url_for('menu'))

        else:
            flash("Invalid OTP. Please try again")
            return render_template('otp_validation.html')

    return render_template('otp_validation.html')


@app.route('/menu', methods=['GET', 'POST'])
def menu():
    # TODO: Logic to get the menu from Database

    if 'user_id' not in session:
        flash("Please log in to continue")
        return redirect(url_for('login'))

    if request.method == 'POST':
        if session['user_mobile'] not in carts:
            carts[session['user_mobile']] = []

        item_id = int(request.form['item_id'])
        item = next((item for item in menu_items if item['menu_id'] == item_id), None)
        if item:
            carts[session['user_mobile']].append(item)
            session['cart'] = carts[session['user_mobile']]
            flash(f"{item['name']} added to the cart.")

    return render_template('menu.html', menu_items=menu_items)


@app.route('/cart', methods=['GET', 'POST'])
def cart_view():
    if 'user_id' not in session:
        flash("Please log in to continue")
        return redirect(url_for('login'))

    total_price = sum(items['price'] for items in carts.get(session['user_mobile'], []))

    if request.method == 'POST':
        # TODO: Logic to insert order details to Orders table
        conn = DBConnection("")
        # conn.execute("")
        # conn.commit()
        # conn.close()

        return redirect(url_for('order_success'))

    return render_template('cart.html', cart=carts[session['user_mobile']], total_price=total_price)


@app.route('/order-success')
def order_success():
    carts.pop(session['user_mobile'], None)
    session.clear()
    return render_template('success.html')


if __name__ == '__main__':
    app.run(debug=True)
