# Python
# from bson import ObjectId
from typing import Union

# FastAPI
from fastapi import APIRouter, Path, Query, Body, Depends
from fastapi import HTTPException, status

# database
from database.mongo_client import MongoDB

# security
from security.auth import get_current_user

# models
from models.user import BaseUser
from models.product import Product, ProductDb

# util
from util.verify import verify_shop_id, verify_product_id_in_shop, verify_owner_of_shop


db_client = MongoDB()

router = APIRouter(
    prefix = "/products"
)

### PATH OPERATIONS ###

## get product ##
@router.get(
    path = "/{shop_id}/{product_id}",
    status_code = status.HTTP_200_OK,
    response_model = ProductDb,
    tags = ["Products"],
    summary = "Get a product in a shop"
)
async def get_product(
    shop_id: str = Path(...),
    product_id: str = Path(...)
):
    verify_product_id_in_shop(product_id, shop_id)

    product = db_client.products_db.find_one({"id": product_id})
    product = ProductDb(**product)

    return product


## get products ##
@router.get(
    path = "/{shop_id}/",
    status_code = status.HTTP_200_OK,
    response_model = list,
    tags = ["Products"],
    summary = "Get products in a shop"
)
async def get_products(
    shop_id: str = Path(...),
    product_name: Union[str, None] = Query(default=None)
):
    verify_shop_id(shop_id)
    if not product_name:
        products = db_client.products_db.find().limit(25)

        return [Product(**data) for data in products]
    
    products = db_client.products_db.find(
        {"name": product_name}
    )
    # if len(products) == 0:
    #     raise HTTPException(
    #         status_code = status.HTTP_400_BAD_REQUEST,
    #         detail = {
    #             "errmsg": "Products not found"
    #         }
    #     )
    
    return [ProductDb(**item) for item in products]


## insert product ##
@router.post(
    path = "/register/{shop_id}",
    status_code = status.HTTP_201_CREATED,
    response_model = ProductDb,
    tags = ["Products"],
    summary = "Insert a product in a shop"
)
async def insert_product(
    shop_id: str = Path(...),
    data: Product = Body(...),
    current_user: BaseUser = Depends(get_current_user)
):
    verify_owner_of_shop(shop_id, current_user.id)
    
    product = ProductDb(**data.model_dump())
    product.shop_id = shop_id

    returned_data = db_client.products_db.insert_one(product.model_dump())
    if not returned_data.acknowledged:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = {
                "errmsg": "Product was not inserted"
            }
        )
    
    product_to_return = db_client.products_db.find_one(
        {"_id": returned_data.inserted_id}
    )
    return ProductDb(**product_to_return)


## update stock of product ##
@router.patch(
    path = "/{shop_id}/{product_id}/update-stock/{stock}",
    status_code = status.HTTP_200_OK,
    response_model = ProductDb,
    tags = ["Products"],
    summary = "Set the stock of a product in a shop"
)
async def set_stock_of_product(
    shop_id: str = Path(...),
    product_id: str = Path(...),
    stock: int = Path(..., gt=0),
    current_user: BaseUser = Depends(get_current_user)
):
    verify_product_id_in_shop(product_id, shop_id)
    verify_owner_of_shop(shop_id, current_user.id)

    returned_data = db_client.products_db.update_one(
        {"id": product_id},
        {"$set": {"stock": stock}}
    )
    if not returned_data.acknowledged:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = {
                "errmsg": "Product was not updated"
            }
        )

    product_to_return = db_client.products_db.find_one({"id": product_id})
    return ProductDb(**product_to_return)
