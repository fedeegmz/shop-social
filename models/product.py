# Python
from bson import ObjectId
from typing import Union

# Pydantic
from pydantic import BaseModel, Field


class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))
    name: str = Field(...)
    price: float = Field(
        ...,
        gt = 0
    )
    stock: int = Field(
        ...,
        gt = 0
    )
    description: Union[str, None] = Field(default=None)
    collection: Union[str, None] = Field(default=None)
    img: Union[str, None] = Field(default=None)

    class Config:
        json_schema_extra = {
            "example": {
                "id": str(ObjectId()),
                "name": "Arc reactor",
                "price": 28.5,
                "stock": 4,
                "description": "A replica of the arc reactor",
                "collection": "Home & Deco",
                "img": "http://example-url.com"
            }
        }

class ProductDb(Product):
    shop_id: Union[str, None] = Field(default=None)