# database
from database.mongo_client import MongoDB


db_client = MongoDB()


def get_white_list_users_id():
    ids = db_client.users_db.find({}, {"id": 1, "_id": 0})
    if not ids:
        return []

    return [data["id"] for data in ids]


def get_white_list_usernames():
    usernames = db_client.users_db.find({}, {"username": 1, "_id": 0})
    if not usernames:
        return []
    
    return [data["username"].lower() for data in usernames]


def get_white_list_shop_id():
    ids = db_client.shops_db.find({}, {"id": 1, "_id": 0})
    if not ids:
        return []

    return [data["id"] for data in ids]


def get_white_list_shop_names():
    names = db_client.shops_db.find({}, {"name": 1, "_id": 0})

    if not names:
        return []
    
    return [data["name"] for data in names]


def get_white_list_product_id_in_shop(shop_id: str):
    products = db_client.products_db.find(
        {
            "shop_id": shop_id
        }
    )

    if not products:
        return []
    return [data["id"] for data in products]

def get_white_list_cart_id(cart_id: str):
    carts = db_client.carts_db.find(
        {},
        {
            "id": 1,
            "_id": 0
        }
    )

    return [data["id"] for data in carts]
