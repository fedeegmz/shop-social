# Python
from random import randint

# FastAPI
from fastapi.testclient import TestClient

# app
from main import app

# database
from database.mongo_client import MongoDB

# models
from models.product import ProductDb

# test
from test.util import get_access_token, assert_equal_productdb


client = TestClient(app)
db_client = MongoDB()

new_product: ProductDb = ProductDb(
    name = f'Test product {str(randint(1000, 9999))}',
    price = randint(1, 1000),
    stock = randint(0, 15),
    description = "This is a test description",
    collection = "Home & Deco",
    img = "http://example-url.com",
    shop_id = "65133250769b9799befb1630"
)
access_token = get_access_token()

class TestProductsRouter:
    """
    Run ```pytest -q test/test_products_router.py```
    """

    def test_insert_valid_product(self):
        """
        Verifica que el endpoint inserta un producto correctamente.  
        - Test: routers > products.py > insert_product()
        - Path: products/register/{shop_id}
        - Method: POST
        - Path param:
            - shop_id: <shop's ID>
        - Header param:
            - Authorization: Bearer <access_token>
        - Body param:
            - data: <Product>
        """
        global access_token
        authorization_param = {
            "Authorization": f'Bearer {access_token}'
        }
        response = client.post(
            url = f'products/register/{"65133250769b9799befb1630"}',
            headers = authorization_param,
            json = new_product.dict()
        )

        if response.status_code != 201:
            assert False
            return
        inserted_product = ProductDb(**response.json())

        assert_equal_productdb(inserted_product, new_product)

    def test_get_product_by_valid_id(self):
        """
        Verifica que el producto es el correcto.  
        - Test: routers > products.py > get_product()
        - Path: products/{shop_id}/{product_id}
        - Method: GET
        - Path param:
            - shop_id: <shop's ID>
            - product_id: <product's ID>
        """
        response = client.get(
            url = f'products/{"65133250769b9799befb1630"}/{new_product.id}',
        )

        if response.status_code != 200:
            assert False
            return
        inserted_product = ProductDb(**response.json())

        assert_equal_productdb(inserted_product, new_product)

    def test_get_product_by_valid_name(self):
        """
        Verifica que el producto es el correcto.  
        - Test: routers > products.py > get_products()
        - Path: products/{shop_id}/
        - Method: GET
        - Path param:
            - shop_id: <shop's ID>
        - Query param:
            - product_name: <product's name>
        """
        param = {
            "product_name": new_product.name.lower()
        }
        response = client.get(
            url = f'products/{new_product.shop_id}/',
            params = param
        )
        
        if response.status_code != 200:
            assert False
            return

        for item in response.json():
            product = ProductDb(**item)
            assert product.name == new_product.name.lower()

    def test_get_less_than_25_products(self):
        """
        Verifica que el endpoint no retorna mas de 25 productos.  
        - Test: routers > products.py > get_products()
        - Path: products/{shop_id}/
        - Method: GET
        - Path param:
            - shop_id: <shop's ID>
        """
        response = client.get(
            url = f'products/{new_product.shop_id}/',
        )

        if response.status_code != 200:
            assert False
            return
        
        assert len(response.json()) <= 25
    
    def test_update_valid_stock_of_product(self):
        """
        Verifica que se actualiza correctamente el stock del producto.  
        - Test: routers > products.py > set_stock_of_product()
        - Path: products/{shop_id}/{product_id}/update-stock/{stock}
        - Method: PATCH
        - Path param:
            - shop_id: <shop's ID>
            - product_id: <product's ID>
            - stock: <new value of stock>
        - Header param:
            - Authorization: Bearer <access_token>
        """
        global access_token
        authorization_param = {
            "Authorization": f'Bearer {access_token}'
        }
        stock = 5
        response = client.patch(
            url = f'products/{new_product.shop_id}/{new_product.id}/update-stock/{str(stock)}',
            headers = authorization_param
        )

        if response.status_code != 200:
            assert False
            return
        inserted_product = ProductDb(**response.json())
        
        assert new_product.id == inserted_product.id
        assert inserted_product.stock == stock
    
    def test_delete_valid_product(self):
        returned_data = db_client.products_db.delete_one(
            {"id": new_product.id}
        )
        if not returned_data.acknowledged:
            assert False
