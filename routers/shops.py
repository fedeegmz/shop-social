# Python
from typing import Union

# FastAPI
from fastapi import APIRouter, Path, Query, Body, Depends
from fastapi import HTTPException, status

# database
from database.mongo_client import MongoDB

# models
from models.user import User
from models.shop import Shop, ShopAll
from models.product import Product

# util
from util.auth import get_current_user
from util.verify import verify_shop_name, verify_shop_id


db_client = MongoDB()

router = APIRouter(
    prefix = "/shops"
)

### PATH OPERATIONS ###

## get shops by ID ##
@router.get(
    path = "/{id}",
    status_code = status.HTTP_200_OK,
    response_model = Shop,
    tags = ["Shops"],
    summary = "Get a shop by ID"
)
async def get_shop(
    id: str = Path(...)
):
    verify_shop_id()

    shop = db_client.shops_db.find_one({"id": id})
    shop = Shop(**shop)

    return shop


## get shops ##
@router.get(
    path = "/",
    status_code = status.HTTP_200_OK,
    response_model = Union[Shop, list],
    tags = ["Shops"],
    summary = "Get a shop or shops"
)
async def get_shops(
    shop_name: Union[str, None] = Query(default=None)
):
    if not shop_name:
        shops = db_client.shops_db.find().limit(25)
        return [Shop(**shop) for shop in shops]

    shop_name = shop_name.lower()
    verify_shop_name(shop_name)
    
    shop = db_client.shops_db.find_one({"name": shop_name}, {"_id": 0})
    products = db_client.products_db.find(
        {
            "shop_name": shop_name,
            "stock": {"$gt": 0}
        }
    )
    print(products[0])
    products = [Product(**product).dict() for product in products]
    print(products)

    shop_to_return = shop
    shop_to_return["products"] = products
    shop_to_return = ShopAll(**shop_to_return)
    return shop_to_return


## insert a new shop ##
@router.post(
    path = "/",
    status_code = status.HTTP_201_CREATED,
    # response_model = Shop,
    tags = ["Shops"],
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
    print(data.dict())

    return data.dict()
