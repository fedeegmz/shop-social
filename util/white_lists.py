# database
from database.mongo_client import MongoDB


db_client = MongoDB()


def get_white_list_usernames():
    to_return = []
    usernames = db_client.users_db.find({}, {"username": 1, "_id": 0})
    
    if not usernames:
        return []
    for username in usernames:
        to_return.append(username.get("username").lower())
    
    return to_return

def get_white_list_name_shops():
    to_return = []
    names = db_client.shops_db.find({}, {"name": 1, "_id": 0})

    if not names:
        return []
    for name in names:
        to_return.append(name.get("name").lower())
    
    return to_return

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