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
    
    return [data["name"].lower() for data in names]


def get_white_list_product_id_in_shop(shop_name: str):
    to_return = []
    shop_name = shop_name.lower()
    products = db_client.products_db.find(
        {
            "shop_name": shop_name
        }
    )

    if not products:
        return []
    for product in products:
        to_return.append(str(product.get("_id")))
    
    return to_return