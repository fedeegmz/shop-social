# Python
from random import randint

# FastAPI
from fastapi.testclient import TestClient

# app
from main import app

# database
from database.mongo_client import MongoDB

# models
from models.cart import Cart
from models.ticket import Ticket

# test
from test.util import get_access_token, insert_product


client = TestClient(app)
db_client = MongoDB()

access_token = get_access_token()
new_product = insert_product()


class TestCartsRouter:
    """
    Run ```pytest -q test/test_carts_router.py```
    """

    def test_add_valid_product(self):
        """
        Verifica que se agrega correctamente el producto al carrito.   
        - Test: routers > carts.py > add_product_to_cart()
        - Path: carts/{shop_id}/{product_id}/add-to-cart
        - Method: POST
        - Path param:
            - shop_id: <shop's ID>
            - product_id: <product's ID>
        - Header param:
            - Authorization: Bearer <access_token>
        """
        authorization_param = {
            "Authorization": f'Bearer {get_access_token()}'
        }
        response = client.post(
            url = f'carts/{new_product.shop_id}/{new_product.id}/add-to-cart',
            headers = authorization_param
        )

        if response.status_code != 202:
            assert False
            return
        returned_cart = Cart(**response.json())

        found = False
        for item in returned_cart.products:
            if item == new_product.id:
                found = True
                break
        if not found:
            assert False
    
    def test_get_my_cart(self):
        """
        Verifica que el endpoint retorna el carrito correcto.  
        - Test: routers > carts.py > get_my_cart()
        - Path: carts/my
        - Method: GET
        - Header param:
            - Authorization: Bearer <access_token>
        """
        authorization_param = {
            "Authorization": f'Bearer {get_access_token()}'
        }
        response = client.get(
            url = "carts/my",
            headers = authorization_param
        )

        if response.status_code != 200:
            assert False
            return
        returned_cart = Cart(**response.json())

        assert returned_cart.user_id == "6515ba03cab17aef182c8a0a"

    def test_buy_my_cart(self):
        """
        Verifica que el endpoint retorna un ticket correcto.   
        - Test: routers > carts.py > buy_cart()
        - Path: carts/my/buy
        - Method: POST
        - Header param:
            - Authorization: Bearer <access_token>
        """
        authorization_param = {
            "Authorization": f'Bearer {get_access_token()}'
        }
        response = client.post(
            url = "carts/my/buy",
            headers = authorization_param
        )
        print(response.json())
        if response.status_code != 202:
            assert False
            return
        ticket = Ticket(**response.json()["ticket"])

        assert ticket.user_id == "6515ba03cab17aef182c8a0a"
        assert ticket.type == "sale"
    
    def test_delete_product(self):
        returned_data = db_client.products_db.delete_one(
            {"id": new_product.id}
        )
        if not returned_data.acknowledged:
            assert False
