# Python
from bson import ObjectId

# FastAPI
from fastapi import APIRouter, Path, Body, Depends
from fastapi import HTTPException, status

# database
from database.mongo_client import MongoDB

# models
from models.user import User
from models.shop import Shop
from models.product import Product, ProductDb

# util
from util.auth import get_current_user
from util.verify import verify_shop_name, verify_product_id_in_shop, verify_owner_of_shop


db_client = MongoDB()

router = APIRouter(
    prefix = "/products"
)

### PATH OPERATIONS ###

## get product ##
@router.get(
    path = "/{shop_name}/{product_id}",
    status_code = status.HTTP_200_OK,
    tags = ["Products"],
    summary = "Get a product in a shop"
)
async def get_product(
    shop_name: str = Path(...),
    product_id: str = Path(...)
):
    verify_shop_name(shop_name)
    verify_product_id_in_shop(product_id, shop_name)

    product = db_client.products_db.find_one({"_id": ObjectId(product_id)})
    product = Product(**product)

    return product

@router.post(
    path = "/{shop_name}/insert-product",
    status_code = status.HTTP_201_CREATED,
    tags = ["Products"],
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

    inserted_id = db_client.products_db.insert_one(product.dict()).inserted_id
    product_to_return = db_client.products_db.find_one({"_id": ObjectId(inserted_id)})

    return Product(**product_to_return)

@router.post(
    path = "/{shop_name}/{product_id}/update-stock/{stock}",
    status_code = status.HTTP_200_OK,
    tags = ["Products"],
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
