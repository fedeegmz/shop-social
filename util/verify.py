# FastAPI
from fastapi import HTTPException, status

# database
from database.mongo_client import MongoDB

# models
from models.shop import Shop

# util
from util.white_lists import get_white_list_usernames, get_white_list_name_shops, get_white_list_product_id_in_shop


db_client = MongoDB()


def verify_username(username: str):
    if not username.lower() in get_white_list_usernames():
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = {
                "errmsg": "Incorrect username"
            }
        )

def verify_shop_name(shop_name: str):
    if not shop_name.lower() in get_white_list_name_shops():
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = {
                "errmsg": "Incorrect name"
            }
        )

def verify_product_id_in_shop(product_id: str, shop_name: str):
    verify_shop_name(shop_name)

    if not product_id in get_white_list_product_id_in_shop(shop_name):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = {
                "errmsg": "Incorrect product"
            }
        )

def verify_owner_of_shop(shop: Shop, username: str):
    shop = db_client.shops_db.find_one({"name": shop.name})

    if not shop.get("owner_username") == username:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = {
                "errmsg": f'You are not the owner of {shop.name.capitalize()}'
            }
        )