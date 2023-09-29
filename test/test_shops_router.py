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
