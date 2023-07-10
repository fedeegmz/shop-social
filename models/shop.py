from pydantic import BaseModel, Field, HttpUrl

# models
from models.product import Product


class Shop(BaseModel):
    name: str = Field(...)
    description: str = Field()
    icon: str = Field()
    owner_username: str = Field(default=None)

class ShopAll(Shop):
    products: list[Product] = Field()