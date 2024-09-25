from flask import Flask, request, jsonify, redirect, url_for, session
from flask_cors import CORS
import random
import logging
import uuid

app = Flask(__name__)
CORS(app)
app.secret_key = 'b121e0dcf1e2e7a0dbeb72284633fd25'

users = {}
carts = {}


@app.route('/login', methods=['POST'])
def send_otp():
    mobile = request.json.get('mobile')

    # TODO: Logic to check if its a valid country number

    if not mobile:
        return jsonify({"error": "Mobile number is required"}), 400

    # Generate random 4-digit OTP
    otp = random.randint(1000, 9999)
    print("mobile - ", otp)

    user_token = str(uuid.uuid4())

    users[mobile] = {'otp': otp, 'verified': False, 'token': user_token}

    # TODO: Logic for sending otp to mobile number

    carts[user_token] = []
    return jsonify({"message": "OTP sent successfully", "token": user_token}), 200


@app.route('/otp-validation/<otp>', methods=['POST'])
def validate_otp(otp):
    mobile = request.json.get('mobile')

    if not mobile or mobile not in users:
        return jsonify({"error": "Mobile number not found"}), 400

    if str(users[mobile]['otp']) == otp:
        users[mobile]['verified'] = True
        return jsonify({"message": "OTP validated successfully"}), 200
    else:
        return jsonify({"error": "Invalid OTP"}), 400


@app.route('/menu', methods=['GET'])
def get_menu():
    # TODO: Logic to get the date from Database

    # For testing in Local - Mock database
    menu = [
        {"name": "Cappuccino", "price": 3.5},
        {"name": "Latte", "price": 4.0},
        {"name": "Espresso", "price": 2.5},
        {"name": "Croissant", "price": 2.0},
        {"name": "Muffin", "price": 2.5}
    ]

    return jsonify(menu), 200


@app.route('/cart', methods=['POST'])
def add_to_cart():
    token = request.json.get('token')
    item_name = request.json.get('name')
    item_price = request.json.get('price')

    if not token or token not in carts:
        return jsonify({"error": "Invalid user token"}), 400

    carts[token].append({"name": item_name, "price": item_price})
    return jsonify({"message": f"{item_name} added to cart"}), 200


@app.route('/cart', methods=['GET'])
def view_cart():
    token = request.args.get('token')

    if not token and token not in carts:
        return jsonify({"error": "Cart not found"}), 400

    return jsonify(carts[token]), 200


@app.route('/place-order', methods=['POST'])
def place_order():
    token = request.json.get('token')

    if not token or not carts[token]:
        return jsonify({"error": "Cart is empty"}), 400

    # TODO: Logic to save order data to Database

    # Clear the token after order is placed
    carts.pop(token, None)

    return jsonify({"message": "Order placed successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)
