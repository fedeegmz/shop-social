# Python
# from bson import ObjectId

# FastAPI
from fastapi import APIRouter, Path, Depends
from fastapi import HTTPException, status

# database
from database.mongo_client import MongoDB

# auth
from auth.auth import get_current_user

# models
from models.user import BaseUser
from models.product import Product
from models.cart import Cart
from models.ticket import Ticket, TypeTicket

# util
from util.verify import verify_product_id_in_shop


db_client = MongoDB()

router = APIRouter(
    prefix = "/carts"
)

### PATH OPERATIONS ###

## get my cart ##
@router.get(
    path = "/my",
    status_code = status.HTTP_200_OK,
    response_model = Cart,
    tags = ["Carts"],
    summary = "Get my cart"
)
async def get_my_cart(current_user: BaseUser = Depends(get_current_user)):
    cart = db_client.carts_db.find_one({"user_id": current_user.id})
    if not cart:
        return None
    return Cart(**cart)


## add product ##
@router.post(
    path = "/{shop_id}/{product_id}/add-to-cart",
    status_code = status.HTTP_202_ACCEPTED,
    response_model = Cart,
    tags = ["Carts"],
    summary = "Add a product in the cart"
)
async def add_product_to_cart(
    shop_id: str = Path(...),
    product_id: str = Path(...),
    current_user: BaseUser = Depends(get_current_user)
):
    verify_product_id_in_shop(product_id, shop_id)

    cart = db_client.carts_db.find_one(
        {
            "user_id": current_user.id
        }
    )
    if not cart:
        cart = Cart(
            user_id = current_user.id
        )
    else:
        cart = Cart(**cart)

    product = db_client.products_db.find_one({"id": product_id})
    product = Product(**product)

    if product.stock == 0:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = {
                "errmsg": "Product without stock"
            }
        )
    
    cart.products.append(product.id)
    cart.total += product.price
    
    # returned_product_data = db_client.products_db.update_one(
    #     filter = {"id": product_id},
    #     update = {"$set": {"stock": product.stock}}
    # )
    # if not returned_product_data.acknowledged:
    #     raise HTTPException(
    #         status_code = status.HTTP_409_CONFLICT,
    #         detail = {
    #             "errmsg": "Product was not inserted"
    #         }
    #     )
    
    returned_cart_data = db_client.carts_db.replace_one(
        filter = {"id": cart.id},
        replacement = cart.dict(),
        upsert = True
    )
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
    path = "/my/buy",
    status_code = status.HTTP_202_ACCEPTED,
    # response_model = Ticket,
    tags = ["Carts"],
    summary = "Buy a cart"
)
async def buy_cart(
    current_user: BaseUser = Depends(get_current_user)
):
    message = f''
    cart_to_buy = db_client.carts_db.find_one({"user_id": current_user.id})
    if not cart_to_buy:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = {
                "errmsg": "You don't have any cart"
            }
        )
    cart_to_buy = Cart(**cart_to_buy)

    ticket = Ticket(
        type = TypeTicket.sale,
        # items = cart_to_buy.products,
        # price = cart_to_buy.total,
        user_id = current_user.id
    )
    
    for item in cart_to_buy.products:
        product = db_client.products_db.find_one({"id": item})
        if not product:
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = {
                    "errmsg": "Product in cart not found"
                }
            )
        product = Product(**product)

        if product.stock == 0:
            cart_to_buy.total -= product.price
            message += f'"{product.id}" deleted because does not have stock, '
            continue
    
        returned_product_data = db_client.products_db.update_one(
            {
                "id": product.id
            },
            {
                "$set": {"stock": product.stock - 1}
            }
        )
        if not returned_product_data.acknowledged:
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = {
                    "errmsg": f'Error with the product: {product.id}'
                }
            )
        ticket.items.append(product)
        ticket.price += product.price

    returned_ticket_data = db_client.tickets_db.insert_one(ticket.dict())
    if not returned_ticket_data:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = {
                "errmsg": "Ticket was not created"
            }
        )

    returned_cart_data = db_client.carts_db.delete_one({"id": cart_to_buy.id})
    if not returned_cart_data.acknowledged:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = {
                "errmsg": "Cart was not bought"
            }
        )

    return {
        "ticket": ticket,
        "message": message
    }
