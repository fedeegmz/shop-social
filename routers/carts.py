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
from util.verify import verify_shop_name, verify_product_id_in_shop, verify_owner_of_shop


db_client = MongoDB()

router = APIRouter(
    prefix = "/cart"
)

### PATH OPERATIONS ###

@router.post(
    path = "/{shop_name}/{product_id}/add-to-cart",
    status_code = status.HTTP_202_ACCEPTED,
    tags = ["Products"],
    summary = "Add a product in the cart",
    response_model = Cart
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

    return cart

@router.post(
    path = "/buy",
    status_code = status.HTTP_200_OK,
    tags = ["Products"],
    summary = "Buy a cart",
    # response_model = Ticket
)
async def buy_cart(
    cart_to_buy: Cart = Body(...)
):
    message = f''
    if not isinstance(cart_to_buy, Cart):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = {
                "errmsg": "Incorrect cart"
            }
        )
    
    for product in cart_to_buy.products:
        if product.stock == 0:
            cart_to_buy.total -= product.price
            message += f'{product.title} deleted because doesn\'t have stock, '
            del product
            continue
    
        db_client.products_db.update_one(
            {
                "_id": ObjectId(product._id)
            },
            {
                "$set": {"stock": {"$inc": -1}}
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
