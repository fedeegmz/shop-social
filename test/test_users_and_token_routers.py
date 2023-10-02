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


class TestUsersAndTokenRouters:
    """
    Run ```pytest -q test/test_users_and_token_routers.py```
    """
    
    def test_insert_valid_user(self):
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

        if response.status_code != 201:
            assert False
            return
        inserted_user = User(**response.json())

        assert_equal_user(inserted_user, new_user)
    
    def test_insert_user_with_invalid_username(self):
        """
        Verifica que no se inserta un usuario con el mismo username.  
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

        assert response.status_code == 409
        assert response.json()["detail"]["errmsg"] == "Username exists"

    def test_get_user_by_valid_id(self):
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
        )

        if response.status_code != 200:
            assert False
            return
        inserted_user = User(**response.json())

        assert_equal_user(inserted_user, new_user)

    def test_get_user_by_invalid_id(self):
        """
        Verifica que el endpoint no retorna un usuario.  
        - Test: routers > users.py > get_user()
        - Path: users/{id}
        - Method: POST
        - Path param:
            - id: <user's ID>
        """
        response = client.get(
            url = f'users/{new_user.id}{randint(100, 999)}'
        )

        assert response.status_code == 400
        assert response.json()["detail"]["errmsg"] == "Incorrect user ID"

    def test_get_user_by_valid_username(self):
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
        )

        if response.status_code != 200:
            assert False
            return
        inserted_user = User(**response.json())

        assert_equal_user(inserted_user, new_user)

    def test_get_user_by_invalid_username(self):
        """
        Verifica que el endpoint no retorna un usuario.  
        - Test: routers > users.py > get_users()
        - Path: users/
        - Method: GET
        - Query param:
            - username: <user's username>
        """
        params = {
            "username": f'{new_user.username}{randint(100, 999)}'
        }
        response = client.get(
            url = "users/",
            params = params
        )

        assert response.status_code == 400
        assert response.json()["detail"]["errmsg"] == "Incorrect username"

    def test_get_less_or_equal_than_25_users(self):
        """
        Verifica que el endpoint no retorna mas de 25 usuarios.  
        - Test: routers > users.py > get_users()
        - Path: users/
        - Method: GET
        """
        response = client.get(
            url = "users/"
        )

        assert response.status_code == 200
        assert len(response.json()) <= 25
        assert len(response.json()) >= 0

    def test_get_access_token_with_a_valid_user(self):
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
        )

        if response.status_code != 202:
            assert False
            return
        response = response.json()

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

    def test_get_access_token_with_a_invalid_user(self):
        """
        Verifica que el endpoint no retorna un access token válido.  
        - Test: routers > token.py > login_for_access_token()
        - Path: login/token
        - Method: POST
        - Form:
            - credentials: <username & password>
        """
        credentials_form = {
            "username": new_user.username,
            "password": f'{new_user.password}{randint(1000, 9999)}'
        }
        response = client.post(
            url = "login/token",
            data = credentials_form
        )

        assert response.status_code == 400
        assert response.json()["detail"]["errmsg"] == "Incorrect username or password"

    def test_get_my_user_info_with_a_valid_access_token(self):
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
        )

        if response.status_code != 200:
            assert False
            return
        inserted_user = BaseUser(**response.json())
        
        assert_equal_base_user(inserted_user, new_user)

    def test_get_my_user_info_with_a_invalid_access_token(self):
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
            "Authorization": f'Bearer {access_token}{randint(100, 999)}'
        }
        response = client.get(
            url = "users/token/me",
            headers = authorization_param
        )

        assert response.status_code == 400
        assert response.json()["detail"]["errmsg"] == "Could not validate credentials"

    def test_delete_valid_user(self):
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
        )

        if response.status_code != 202:
            assert False
            return
        deleted_user = BaseUser(**response.json())

        assert_equal_base_user(deleted_user, new_user)

        returned_data = db_client.users_db.delete_one({"id": new_user.id})
        if not returned_data.acknowledged:
            assert False

    def test_delete_invalid_user(self):
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
            "Authorization": f'Bearer {access_token}{randint(100, 999)}'
        }
        response = client.delete(
            url = "users",
            headers = authorization_param
        )

        assert response.status_code == 400
        assert response.json()["detail"]["errmsg"] == "Could not validate credentials"
