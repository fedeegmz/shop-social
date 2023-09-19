# FastAPI
from fastapi import HTTPException, status

# database
from database.mongo_client import MongoDB

# models
from models.shop import Shop

# util
from util.white_lists import get_white_list_users_id, get_white_list_usernames, get_white_list_product_id_in_shop
from util.white_lists import get_white_list_shop_id, get_white_list_shop_names
from util.white_lists import get_white_list_cart_id


db_client = MongoDB()


def verify_user_id(id: str):
    if not id in get_white_list_users_id():
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = {
                "errmsg": "Incorrect user ID"
            }
        )

def verify_username(username: str):
    if not username.lower() in get_white_list_usernames():
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = {
                "errmsg": "Incorrect username"
            }
        )

def verify_shop_id(id: str):
    if not id in get_white_list_shop_id():
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = {
                "errmsg": "Incorrect shop ID"
            }
        )

def verify_shop_name(shop_name: str):
    if not shop_name.lower() in get_white_list_shop_names():
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = {
                "errmsg": "Incorrect name"
            }
        )

def verify_product_id_in_shop(product_id: str, shop_id: str):
    verify_shop_id(shop_id)

    if not product_id in get_white_list_product_id_in_shop(shop_id):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = {
                "errmsg": "Incorrect product"
            }
        )

def verify_owner_of_shop(shop_id: str, username: str):
    shop = db_client.shops_db.find_one({"id": shop_id})

    if not shop.get("owner_username") == username:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = {
                "errmsg": f'You are not the owner of {shop.name.capitalize()}'
            }
        )

def verify_cart_id(id: str):
    if not id in get_white_list_cart_id():
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = {
                "errmsg": "Incorrect cart ID"
            }
        )
