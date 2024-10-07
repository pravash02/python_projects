from cafe_web.libs.models import db, User, MenuItem, OrderItem, Order


def get_menu_data(menu_items):
    menu_items_dict = [
        {column.name: getattr(item, column.name) for column in MenuItem.__table__.columns}
        for item in menu_items
    ]

    return menu_items_dict
