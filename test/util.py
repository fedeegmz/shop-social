# Python
import os

# FastAPI
from fastapi.testclient import TestClient

# app
from main import app

# models
from models.user import BaseUser, User
from models.shop import BaseShop, Shop


client = TestClient(app)


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
