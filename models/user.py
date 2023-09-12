# Python
from datetime import date
from bson import ObjectId

# Pydantic
from pydantic import BaseModel, Field


class User(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))
    username: str = Field(
        ...,
        min_length = 4,
        max_length = 15
    )
    name: str = Field(
        ...,
        min_length = 3,
        max_length = 20
    )
    lastname: str = Field(
        ...,
        min_length = 3,
        max_length = 20
    )

class UserDb(User):
    disabled: bool = Field(default=False)
    created: str = Field(default=str(date.today()))
    is_superuser: bool = Field(default=False)

class UserIn(UserDb):
    password: str = Field(
        ...,
        min_length = 8,
        max_length = 64
    )