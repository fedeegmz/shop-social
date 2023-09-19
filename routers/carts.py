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
from models.cart import Cart
from models.ticket import Ticket, TypeTicket

# util
from util.auth import get_current_user
from util.verify import verify_shop_id, verify_product_id_in_shop, verify_cart_id


db_client = MongoDB()

router = APIRouter(
    prefix = "/cart"
)

### PATH OPERATIONS ###

## add product ##
@router.post(
    path = "/{shop_id}/{product_id}/add-to-cart",
    status_code = status.HTTP_202_ACCEPTED,
    tags = ["Products"],
    summary = "Add a product in the cart",
    response_model = Cart
)
async def add_product_to_cart(
    shop_id: str = Path(...),
    product_id: str = Path(...),
    current_user: User = Depends(get_current_user)
):
    verify_shop_id(shop_id)
    verify_product_id_in_shop(product_id, shop_id)

    cart = db_client.carts_db.find_one(
        {
            "user_id": current_user.id
        }
    )
    cart = Cart(**cart)
    if not cart:
        cart = Cart(
            user_id = current_user.id
        )

    product = db_client.products_db.find_one(
        {
            "id": product_id
        }
    )
    product = Product(**product)

    if product.stock == 0:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = {
                "errmsg": "Product without stock"
            }
        )
    
    cart.products.append(product)
    for item in cart.products:
        cart.total += item.price
    
    returned_product_data = db_client.products_db.update_one(
        filter = {"id": product_id},
        update = {"$set": {"$inc": {"stock": -1}}}
    )
    if not returned_product_data.acknowledged:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = {
                "errmsg": "Product was not inserted"
            }
        )
    
    returned_cart_data = db_client.carts_db.insert_one(cart)
    if not returned_cart_data.acknowledged:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = {
                "errmsg": "Cart was not inserted"
            }
        )

    return cart


## buy the cart ##
@router.post(
    path = "/buy/{cart_id}",
    status_code = status.HTTP_200_OK,
    tags = ["Products"],
    summary = "Buy a cart",
    # response_model = Ticket
)
async def buy_cart(
    cart_id: str = Path(...)
):
    verify_cart_id(cart_id)
    message = f''
    cart_to_buy = db_client.carts_db.find_one({"id": cart_id})
    cart_to_buy = Cart(**cart_to_buy)
    
    for product in cart_to_buy.products:
        # if product.stock == 0:
        #     cart_to_buy.total -= product.price
        #     message += f'{product.title} deleted because does not have stock, '
        #     del product
        #     continue
    
        returned_product_data = db_client.products_db.update_one(
            {
                "id": product.id
            },
            {
                "$set": {"$inc": {"stock": -1}}
            }
        )
        if not returned_product_data.acknowledged:
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = {
                    "errmsg": "Cart was not bought"
                }
            )

    ticket = Ticket(
        type = TypeTicket.sale,
        items = cart_to_buy.products,
        price = cart_to_buy.total
    )

    return {
        "ticket": ticket,
        "message": message
    }
