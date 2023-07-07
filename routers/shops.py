from bson import ObjectId
# FastAPI
from fastapi import APIRouter, Path, Query, Body, Depends
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

# database
from database.mongo_client import db_client

# models
from models.user import User
from models.shop import Shop
from models.product import Product, ProductDb
from models.cart import Cart

# util
from util.auth import get_current_user
from util.white_lists import get_white_list_name_shops
from util.verify import verify_shop_name, verify_product_id_in_shop, verify_owner_of_shop


router = APIRouter(
    prefix = "/shops"
)

@router.get(
    path = "/",
    status_code = status.HTTP_200_OK,
    tags = ["shops"],
    summary = "Get all shops"
)
async def get_shops():
    shops = db_client.shops_db.find()
    return [Shop(**shop) for shop in shops]

@router.get(
    path = "/{shop_name}",
    status_code = status.HTTP_200_OK,
    tags = ["shops"],
    summary = "Get a shop"
)
async def get_shop(
    shop_name: str = Path(...)
):
    shop_name = shop_name.lower()
    verify_shop_name(shop_name)
    
    shop = db_client.shops_db.find_one({"name": shop_name}, {"_id": 0})
    print(shop)
    return shop

@router.post(
    path = "/",
    status_code = status.HTTP_201_CREATED,
    tags = ["shops"],
    summary = "Insert a shop"
)
async def insert_shop(
    data: Shop = Body(...),
    current_user: User = Depends(get_current_user)
):
    if not isinstance(Shop(**data.dict()), Shop):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = {
                "errmsg": "Incorrect shop data"
            }
        )
    
    data.name = data.name.lower()
    data.owner_username = current_user.username
    db_client.shops_db.insert_one(data.dict())

    return data.dict()

@router.post(
    path = "/{shop_name}/insert-product",
    status_code = status.HTTP_201_CREATED,
    tags = ["shops"],
    summary = "Insert a product in a shop"
)
async def insert_product_in_shop(
    shop_name: str = Path(...),
    data: Product = Body(...),
    current_user: User = Depends(get_current_user)
):
    verify_shop_name(shop_name)
    if not isinstance(Product(**data.dict()), Product):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = {
                "errmsg": "Incorrect product"
            }
        )
    
    shop = db_client.shops_db.find_one({"name": shop_name})
    shop = Shop(**shop)

    verify_owner_of_shop(shop, current_user.username)
    
    product = data.dict()
    product["shop_name"] = shop.name
    product = ProductDb(**product)

    db_client.products_db.insert_one(product.dict())

    return product

@router.post(
    path = "/{shop_name}/{product_id}/update-stock/{stock}",
    status_code = status.HTTP_200_OK,
    tags = ["shops"],
    summary = "Set the stock of a product in a shop"
)
async def set_stock_of_product(
    shop_name: str = Path(...),
    product_id: str = Path(...),
    stock: int = Path(...),
    current_user: User = Depends(get_current_user)
):
    verify_shop_name(shop_name)
    verify_product_id_in_shop(product_id, shop_name)
    shop = db_client.shops_db.find({"name": shop_name})
    shop = Shop(**shop)
    verify_owner_of_shop(shop, current_user)
    if not isinstance(stock, int):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = {
                "errmsg": "Incorrect number of stock"
            }
        )

    product = db_client.products_db.__find_and_modify(
        {
            "query": {
                "_id": ObjectId(product_id)
            },
            "update": {
                "$set": {"stock": stock}
            },
            "new": True
        }
    )

    return product


### BUY OPERATIONS ###

@router.post(
    path = "/{shop_name}/{product_id}/add-to-cart",
    status_code = status.HTTP_202_ACCEPTED,
    tags = ["shops"],
    summary = "Add a product in the cart"
)
async def add_product_to_cart(
    shop_name: str = Path(...),
    product_id: str = Path(...),
    products_list: list[Product] = Body(default=[]),
    current_user: User = Depends(get_current_user)
):
    shop_name = shop_name.lower()
    verify_shop_name(shop_name)
    verify_product_id_in_shop(product_id, shop_name)
    cart = Cart(
        owner = current_user,
        products = [Product(**_product.dict()) for _product in products_list],
        total = 0
    )

    product = db_client.products_db.find(
        {
            "_id": ObjectId(product_id)
        }
    )

    if product.stock == 0:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = {
                "errmsg": "Product without stock"
            }
        )
    
    cart.products.append(Product(**product))
    for product_ in cart.products:
        cart.total += product_.price
    product.stock -= 1

    db_client.products_db.update_one(
        {
            "_id": ObjectId(product_id)
        },
        {
            "$set": {"stock": {"$inc": -1}}
        }
    )

    return cart