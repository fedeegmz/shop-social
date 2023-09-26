# Python
from bson import ObjectId
from typing import Union

# Pydantic
from pydantic import BaseModel, Field

# models
from models.user import User
from models.product import Product


class Cart(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))
    user_id: str = Field(...)
    products: Union[list[str], list] = Field(default=[])
    total: float = Field(default=0)