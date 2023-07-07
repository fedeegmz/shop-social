from pydantic import BaseModel, Field

# models
from models.user import User
from models.product import Product


class Cart(BaseModel):
    owner: User = Field(...)
    products: list[Product] = Field(default=[])
    total: float = Field()