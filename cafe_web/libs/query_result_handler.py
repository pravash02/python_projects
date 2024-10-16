from cafe_web.libs.models import db, User, MenuItem, OrderItem, Order, CartItem


def get_menu_data(menu_items):
    menu_items_dict = [
        {column.name: getattr(item, column.name) for column in MenuItem.__table__.columns}
        for item in menu_items
    ]

    return menu_items_dict


def get_cart_data(menu_items):
    cart_items_dict = [
        {column.name: getattr(item, column.name) for column in CartItem.__table__.columns}
        for item in menu_items
    ]

    return cart_items_dict
