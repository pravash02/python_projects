import os
import logging
from flask import Flask
from cafe_web.libs.models import db, MenuItem

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'postgresql://pravashpanigrahi:prav%400411@localhost/prav'
db.init_app(app)

# Mock Data for Food and Drinks
menu_items = [
    {'name': 'Cappuccino', 'category': 'Coffee', 'price': 5, 'photo': ''},
    {'name': 'Latte', 'category': 'Coffee', 'price': 4, 'photo': ''},
    {'name': 'Mocha', 'category': 'Coffee', 'price': 6, 'photo': ''},
    {'name': 'Hazelnut', 'category': 'Flavoured Coffee', 'price': 4.5, 'photo': ''},
    {'name': 'Caramel', 'category': 'Flavoured Coffee', 'price': 4.5, 'photo': ''},
    {'name': 'Mocha', 'category': 'Flavoured Coffee', 'price': 3.5, 'photo': ''},
    {'name': 'Cinnamon', 'category': 'Flavoured Coffee', 'price': 4, 'photo': ''},
    {'name': 'Peppermint', 'category': 'Flavoured Coffee', 'price': 3.5, 'photo': ''},
    {'name': 'Chocolate Brownie', 'category': 'Pastry', 'price': 3, 'photo': ''},
    {'name': 'Caramel shortbread', 'category': 'Pastry', 'price': 5, 'photo': ''},
    {'name': 'Chocolate Truffle', 'category': 'Pastry', 'price': 2.8, 'photo': ''},
    {'name': 'Croissant', 'category': 'Pastry', 'price': 3.5, 'photo': ''},
    {'name': 'Chocolate Cookies', 'category': 'Pastry', 'price': 3.1, 'photo': ''},
    {'name': 'Honey & Raisin Cake', 'category': 'Pastry', 'price': 3, 'photo': ''},
    {'name': 'Muffins', 'category': 'Pastry', 'price': 2.4, 'photo': ''},
]


# Create a function to insert the menu items
def insert_menu_items():
    try:
        for item in menu_items:
            new_item = MenuItem(
                name=item['name'],
                category=item['category'],
                price=item['price'],
                photo=item['photo']
            )
            db.session.add(new_item)
        db.session.commit()
        logging.info("Menu items inserted successfully.")

    except Exception as e:
        db.session.rollback()
        logging.error(f"Error inserting menu items: {str(e)}")


# Call the function to insert data
if __name__ == '__main__':
    with app.app_context():
        insert_menu_items()
        print("Menu Items inserted successfully.")
