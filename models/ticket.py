from datetime import date, datetime
from pydantic import BaseModel, Field


class Ticket(BaseModel):
    release_date: date = Field(
        ...,
        default_factory = lambda: datetime.now()
    )
    type: str = Field()
    items: list = Field(default=None)
    price: float = Field(...)