# Python
from random import randint

# FastAPI
from fastapi.testclient import TestClient

# app
from main import app

# models
from models.shop import Shop

# test
from test.util import get_access_token, assert_equal_shop


client = TestClient(app)

new_shop: Shop = Shop(
    name = f'TestShop{str(randint(1000, 9999))}',
    description = "This is an example description to test the endpoints",
    icon = "http://example-url.com",
    owner_id = "6515ba03cab17aef182c8a0a"
)
access_token = get_access_token()

class TestShopsRouter:
    """
    Run ```pytest -q test/test_shops_router.py```
    """

    def test_insert_valid_shop(self):
        """
        Verifica que la tienda insertada es igual a la que retorna el endpoint.  
        - Test: routers > shops.py > insert_shop()
        - Path: shops/register
        - Method: POST
        - Header param:
            - Authorization: Bearer <access_token>
        - Body param:
            - data: <BaseShop>
        """
        global access_token
        authorization_param = {
            "Authorization": f'Bearer {access_token}'
        }
        response = client.post(
            url = "shops/register",
            headers = authorization_param,
            json = new_shop.dict()
        )

        if response.status_code != 201:
            assert False
            return
        inserted_shop = Shop(**response.json())

        assert_equal_shop(inserted_shop, new_shop)
    
    def test_insert_shop_with_invalid_name(self):
        """
        Verifica que no se inserta una tienda con el mismo nombre.  
        - Test: routers > shops.py > insert_shop()
        - Path: shops/register
        - Method: POST
        - Header param:
            - Authorization: Bearer <access_token>
        - Body param:
            - data: <BaseShop>
        """
        global access_token
        authorization_param = {
            "Authorization": f'Bearer {access_token}'
        }
        response = client.post(
            url = "shops/register",
            headers = authorization_param,
            json = new_shop.dict()
        )

        assert response.status_code == 400
        assert response.json()["detail"]["errmsg"] == "Shop's name exist"

    def test_get_shop_by_valid_id(self):
        """
        Verifica que el endpoint retorna la tienda correcta.  
        - Test: routers > shops.py > get_shop()
        - Path: shops/{id}
        - Method: GET
        - Path param:
            - id: <shop's ID>
        """
        response = client.get(
            url = f'shops/{new_shop.id}'
        )

        if response.status_code != 200:
            assert False
            return
        inserted_shop = Shop(**response.json())

        assert_equal_shop(inserted_shop, new_shop)
    
    def test_get_shop_by_invalid_id(self):
        """
        Verifica que el endpoint no retorna una tienda.  
        - Test: routers > shops.py > get_shop()
        - Path: shops/{id}
        - Method: GET
        - Path param:
            - id: <shop's ID>
        """
        response = client.get(
            url = f'shops/{new_shop.id}{randint(100, 999)}'
        )

        assert response.status_code == 400
        assert response.json()["detail"]["errmsg"] == "Incorrect shop ID"

    def test_get_shop_by_valid_name(self):
        """
        Verifica que el endpoint retorna la tienda correcta.  
        - Test: routers > shops.py > get_shops()
        - Path: shops/
        - Method: GET
        - Query param:
            - name: <shop's name>
        """
        param = {
            "name": new_shop.name.lower()
        }
        response = client.get(
            url = "shops",
            params = param
        )

        if response.status_code != 200:
            assert False
            return
        inserted_shop = Shop(**response.json())

        assert_equal_shop(inserted_shop, new_shop)
    
    def test_get_shop_by_invalid_name(self):
        """
        Verifica que el endpoint no retorna una tienda.  
        - Test: routers > shops.py > get_shops()
        - Path: shops/
        - Method: GET
        - Query param:
            - name: <shop's name>
        """
        param = {
            "name": f'{new_shop.name.lower()}{randint(100, 999)}'
        }
        response = client.get(
            url = "shops",
            params = param
        )

        assert response.status_code == 400
        assert response.json()["detail"]["errmsg"] == "Incorrect name"
    
    def test_get_less_or_equal_than_25_shops(self):
        """
        Verifica que el endpoint no retorna mas de 25 tiendas.  
        - Test: routers > shops.py > get_shops()
        - Path: shops/
        - Method: GET
        """
        response = client.get(
            url = "shops"
        )

        assert response.status_code == 200
        assert len(response.json()) <= 25
        assert len(response.json()) >= 0

    def test_delete_valid_shop(self):
        """
        Verifica que el endpoint elimina la tienda.  
        - Test: routers > shops.py > delete_shop()
        - Path: shops/{id}
        - Method: DELETE
        - Path param:
            - id: <shop's ID>
        - Header param:
            - Authorization: Bearer <access_token>
        """
        global access_token
        authorization_param = {
            "Authorization": f'Bearer {access_token}'
        }
        response = client.delete(
            url = f'shops/{new_shop.id}',
            headers = authorization_param
        )

        if response.status_code != 202:
            assert False
            return

        assert response.json() == True

    def test_delete_invalid_shop(self):
        """
        Verifica que el endpoint no elimina una tienda.  
        - Test: routers > shops.py > delete_shop()
        - Path: shops/{id}
        - Method: DELETE
        - Path param:
            - id: <shop's ID>
        - Header param:
            - Authorization: Bearer <access_token>
        """
        global access_token
        authorization_param = {
            "Authorization": f'Bearer {access_token}{randint(100, 999)}'
        }
        response = client.delete(
            url = f'shops/{new_shop.id}',
            headers = authorization_param
        )

        assert response.status_code == 400
        assert response.json()["detail"]["errmsg"] == "Could not validate credentials"
