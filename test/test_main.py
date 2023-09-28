# Python
import os
from random import randint

# FastAPI
from fastapi.testclient import TestClient

# JWT
from jose import jwt

# app
from main import app

# database
from database.mongo_client import MongoDB

# models
from models.user import BaseUser, User, UserDb

# test
from test.util import assert_equal_base_user, assert_equal_user


client = TestClient(app)
db_client = MongoDB()
JWT_SECRETKEY = os.getenv("JWT_SECRETKEY")
ALGORITHM = "HS256"

new_user: UserDb = UserDb(
    username = f'test+{str(randint(1000, 9999))}',
    name = "TestUser",
    lastname = "TestUser",
    password = f'password+{str(randint(1000, 9999))}'
)
access_token: str = ""


### USERS & TOKEN ###

def test_insert_valid_user():
    """
    Verifica que el usuario que se envía al endpoint sea igual al que retorna el endpoint.  
    - Test: routers > users.py > create_user()
    - Path: users/register
    - Method: POST
    - Body param:
        - data: <UserDb>
    """
    response = client.post(
        url = "users/register",
        json = new_user.dict()
    )
    inserted_user = User(**response.json())

    assert_equal_user(inserted_user, new_user)
    
def test_get_user_by_valid_id():
    """
    Verifica que el endpoint retorna el usuario correcto.  
    - Test: routers > users.py > get_user()
    - Path: users/{id}
    - Method: POST
    - Path param:
        - id: <user's ID>
    """
    response = client.get(
        url = f'users/{new_user.id}'
    ).json()
    inserted_user = User(**response)

    assert_equal_user(inserted_user, new_user)

def test_get_user_by_valid_username():
    """
    Verifica que el endpoint retorna el usuario correcto.  
    - Test: routers > users.py > get_users()
    - Path: users/
    - Method: GET
    - Query param:
        - username: <user's username>
    """
    params = {
        "username": new_user.username
    }
    response = client.get(
        url = "users/",
        params = params
    ).json()
    inserted_user = User(**response)

    assert_equal_user(inserted_user, new_user)

def test_get_access_token_with_a_valid_user():
    """
    Verifica que el endpoint retorna un access token válido.  
    - Test: routers > token.py > login_for_access_token()
    - Path: login/token
    - Method: POST
    - Form:
        - credentials: <username & password>
    """
    credentials_form = {
        "username": new_user.username,
        "password": new_user.password
    }
    response = client.post(
        url = "login/token",
        data = credentials_form
    ).json()

    try:
        global access_token
        access_token = response["access_token"]
        payload = jwt.decode(access_token, JWT_SECRETKEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
    except:
        assert False
    
    assert str(type(response)) == "<class 'dict'>"
    assert username == new_user.username
    assert response.get("token_type", "") == "bearer"

def test_get_my_user_info_with_a_valid_access_token():
    """
    Verifica que el endpoint retorna la información de usuario con un access token válido.  
    - Test: routers > users.py > read_users_me()
    - Path: users/token/me
    - Method: GET
    - Header param:
        - Authorization: Bearer <access_token>
    """
    global access_token
    authorization_param = {
        "Authorization": f'Bearer {access_token}'
    }
    response = client.get(
        url = "users/token/me",
        headers = authorization_param
    ).json()
    inserted_user = BaseUser(**response)
    
    assert_equal_base_user(inserted_user, new_user)

def test_delete_valid_user():
    """
    Verifica que se elimina mi usuario.  
    - Test: routers > users.py > delete_user()
    - Path: users/
    - Method: DELETE
    - Header param:
        - Authorization: Bearer <access_token>
    """
    global access_token
    authorization_param = {
        "Authorization": f'Bearer {access_token}'
    }
    response = client.delete(
        url = "users",
        headers = authorization_param
    ).json()
    deleted_user = BaseUser(**response)

    assert_equal_base_user(deleted_user, new_user)
