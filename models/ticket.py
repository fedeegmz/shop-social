# Python
from enum import Enum
from datetime import date, datetime
from bson import ObjectId
from typing import Union

# Pydantic
from pydantic import BaseModel, Field


class TypeTicket(str, Enum):
    sale = "sale"
    purchase = "purchase"

class Ticket(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))
    user_id: Union[str, None] = Field(default=None)
    release_date: date = Field(default_factory = lambda: datetime.now())
    type: TypeTicket = Field()
    items: list = Field(default_factory=lambda: [])
    price: float = Field(default=0)
