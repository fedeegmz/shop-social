# Python
from enum import Enum
from datetime import date, datetime
from bson import ObjectId

# Pydantic
from pydantic import BaseModel, Field


class TypeTicket(str, Enum):
    sale = "sale"
    purchase = "purchase"

class Ticket(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))
    release_date: date = Field(
        ...,
        default_factory = lambda: datetime.now()
    )
    type: TypeTicket = Field()
    items: list = Field(default=[])
    price: float = Field(...)