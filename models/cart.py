# Python
from bson import ObjectId

# Pydantic
from pydantic import BaseModel, Field

# models
from models.user import User
from models.product import Product


class Cart(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))
    owner_id: str = Field(...)
    products: list[Product] = Field(default=[])
    total: float = Field()