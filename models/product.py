# Python
from bson import ObjectId
from typing import Union

# Pydantic
from pydantic import BaseModel, Field


class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))
    title: str = Field(...)
    price: float = Field(...)
    stock: int = Field(...)
    description: Union[str, None] = Field(default=None)
    colection: Union[str, None] = Field(default=None)
    img: Union[str, None] = Field(default=None)

class ProductDb(Product):
    shop_name: str = Field(...)