# Python
import os
from random import randint

# FastAPI
from fastapi.testclient import TestClient

# app
from main import app

# database
from database.mongo_client import MongoDB

# models
from models.user import BaseUser, User
from models.shop import Shop
from models.product import Product, ProductDb


client = TestClient(app)
db_client = MongoDB()


def get_access_token():
    credentials_form = {
        "username": "testuser+27364",
        "password": os.getenv("PASSWORD_FOR_TESTING")
    }
    response = client.post(
        url = "login/token",
        data = credentials_form
    ).json()

    return response["access_token"]

def insert_product():
    authorization_param = {
        "Authorization": f'Bearer {get_access_token()}'
    }
    product = Product(
        name = f'Test product {str(randint(1000, 9999))}',
        price = randint(0, 200),
        stock = randint(0, 10),
        description = "This a test description",
        collection = "Home & Deco",
        img = "http://example-url.com"
    )
    response = client.post(
        url = f'products/register/{"65133250769b9799befb1630"}',
        headers = authorization_param,
        json = product.dict()
    )

    if response.status_code == 201:
        return ProductDb(**response.json())


def assert_equal_user(user_1: User, user_2: User):
    assert user_1.id == user_2.id
    assert user_1.username == user_2.username
    assert user_1.name == user_2.name
    assert user_1.lastname == user_2.lastname
    assert user_1.disabled == user_2.disabled
    assert user_1.created == user_2.created
    assert user_1.is_superuser == user_2.is_superuser

def assert_equal_base_user(user_1: BaseUser, user_2: BaseUser):
    assert user_1.id == user_2.id
    assert user_1.username == user_2.username
    assert user_1.name == user_2.name
    assert user_1.lastname == user_2.lastname

def assert_equal_base_shop(shop_1: Shop, shop_2: Shop):
    assert shop_1.id == shop_2.id
    assert shop_1.name.lower() == shop_2.name.lower()
    assert shop_1.description == shop_2.description
    assert shop_1.icon == shop_2.icon

def assert_equal_shop(shop_1: Shop, shop_2: Shop):
    assert shop_1.id == shop_2.id
    assert shop_1.name.lower() == shop_2.name.lower()
    assert shop_1.description == shop_2.description
    assert shop_1.icon == shop_2.icon
    assert shop_1.owner_id == shop_2.owner_id

def assert_equal_productdb(product_1: ProductDb, product_2: ProductDb):
    assert product_1.id == product_2.id
    assert product_1.name == product_2.name
    assert product_1.price == product_2.price
    assert product_1.stock == product_2.stock
    assert product_1.description == product_2.description
    assert product_1.collection == product_2.collection
    assert product_1.img == product_2.img
    assert product_1.shop_id == product_2.shop_id
