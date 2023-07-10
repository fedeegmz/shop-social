# FastAPI
from fastapi import APIRouter, Path, Body, Depends
from fastapi import HTTPException, status

# database
from database.mongo_client import MongoDB

# models
from models.user import User
from models.shop import Shop, ShopAll
from models.product import Product

# util
from util.auth import get_current_user
from util.verify import verify_shop_name


db_client = MongoDB()

router = APIRouter(
    prefix = "/shops"
)

@router.get(
    path = "/",
    status_code = status.HTTP_200_OK,
    tags = ["Shops"],
    summary = "Get all shops"
)
async def get_shops():
    shops = db_client.shops_db.find()
    return [Shop(**shop) for shop in shops]

@router.get(
    path = "/{shop_name}",
    status_code = status.HTTP_200_OK,
    tags = ["Shops"],
    summary = "Get a shop"
)
async def get_shop(
    shop_name: str = Path(...)
):
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

@router.post(
    path = "/",
    status_code = status.HTTP_201_CREATED,
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

    return data.dict()
