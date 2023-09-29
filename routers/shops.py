# Python
from typing import Union

# FastAPI
from fastapi import APIRouter, Path, Query, Body, Depends
from fastapi import HTTPException, status

# database
from database.mongo_client import MongoDB

# auth
from auth.auth import get_current_user

# models
from models.user import BaseUser
from models.shop import BaseShop, Shop

# util
from util.verify import verify_shop_name, verify_shop_id
from util.white_lists import get_white_list_shop_names


db_client = MongoDB()

router = APIRouter(
    prefix = "/shops"
)

### PATH OPERATIONS ###

## get shop by ID ##
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
    verify_shop_id(id)

    shop = db_client.shops_db.find_one({"id": id})
    shop = Shop(**shop)

    return shop


## get shops or a shop by name ##
@router.get(
    path = "/",
    status_code = status.HTTP_200_OK,
    response_model = Union[Shop, list],
    tags = ["Shops"],
    summary = "Get a shop or shops"
)
async def get_shops(
    name: Union[str, None] = Query(default=None)
):
    if not name:
        shops = db_client.shops_db.find().limit(25)
        return [Shop(**shop) for shop in shops]

    verify_shop_name(name)
    
    shop = db_client.shops_db.find_one({"name": name})
    if not shop:
        return None
    
    return Shop(**shop)


## insert a shop ##
@router.post(
    path = "/register",
    status_code = status.HTTP_201_CREATED,
    response_model = Shop,
    tags = ["Shops"],
    summary = "Insert a shop"
)
async def insert_shop(
    data: BaseShop = Body(...),
    current_user: BaseUser = Depends(get_current_user)
):
    if data.name in get_white_list_shop_names():
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = {
                "errmsg": "Shop's name exist"
            }
        )
    
    shop = Shop(**data.dict())
    shop.owner_id = current_user.id
    shop.name = data.name.lower()
    
    returned_data = db_client.shops_db.insert_one(shop.dict())
    if not returned_data.acknowledged:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = {
                "errmsg": "Shop not inserted"
            }
        )
    
    shop_to_return = db_client.shops_db.find_one({"_id": returned_data.inserted_id})
    return Shop(**shop_to_return)


## delete a shop ##
@router.delete(
    path = "/{id}",
    status_code = status.HTTP_202_ACCEPTED,
    response_model = bool,
    tags = ["Shops"],
    summary = "Delete my shop"
)
async def insert_shop(
    id: str = Path(...),
    current_user: BaseUser = Depends(get_current_user)
):
    verify_shop_id(id)

    owner_shop = db_client.shops_db.find_one({"id": id}, {"owner_id": 1})

    if not owner_shop["owner_id"] == current_user.id:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = {
                "errmsg": "You are not the owner of the shop"
            }
        )
    
    returned_data = db_client.shops_db.delete_one({"id": id})
    if not returned_data.acknowledged:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = {
                "errmsg": "Shop was not deleted"
            }
        )
    
    return True
