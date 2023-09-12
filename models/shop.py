# Python
from bson import ObjectId
from typing import Union

# Pydantic
from pydantic import BaseModel, Field, HttpUrl

# models
from models.product import Product


class Shop(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))
    name: str = Field(...)
    description: Union[str, None] = Field(default=None)
    icon: Union[HttpUrl, None] = Field(default=None)
    owner_id: Union[str, None] = Field(default=None)

class ShopAll(Shop):
    products: list[Product] = Field()