from bson import ObjectId
from typing import Optional
from pydantic import BaseModel, Field


class Product(BaseModel):
    # _id: ObjectId = Field(default_factory=lambda x: ObjectId(x))
    _id: ObjectId = Field(...)
    title: str = Field(...)
    price: float = Field(...)
    stock: int = Field(...)
    description: Optional[str] = Field(default=None)
    colection: Optional[str] = Field(default=None)
    img: Optional[str] = Field(default=None)

class ProductDb(Product):
    shop_name: str = Field(...)