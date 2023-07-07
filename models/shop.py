from pydantic import BaseModel, Field


class Shop(BaseModel):
    name: str = Field(...)
    description: str = Field()
    icon: str = Field()
    owner_username: str = Field(default=None)