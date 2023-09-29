# Python
from bson import ObjectId
from typing import Union

# Pydantic
from pydantic import BaseModel, Field, HttpUrl

# models
from models.product import Product


class BaseShop(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))
    name: str = Field(default_factory=lambda x: str(x).lower())
    description: Union[str, None] = Field(default=None)
    icon: Union[HttpUrl, None] = Field(default=None)
    
    class Config:
        schema_extra = {
            "example": {
                "id": str(ObjectId()),
                "name": "Stark Industries",
                "description": "The shop of Tony Stark",
                "icon": None

            }
        }

class Shop(BaseShop):
    owner_id: Union[str, None] = Field(default=None)

class ShopAll(Shop):
    products: list[Product] = Field()