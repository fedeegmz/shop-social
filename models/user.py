# Python
from datetime import date
from bson import ObjectId

# Pydantic
from pydantic import BaseModel, Field


class BaseUser(BaseModel):
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

class User(BaseUser):
    disabled: bool = Field(default=False)
    created: str = Field(default=str(date.today()))
    is_superuser: bool = Field(default=False)

class UserDb(User):
    password: str = Field(
        ...,
        min_length = 8,
        max_length = 64
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": str(ObjectId()),
                "username": "ironman",
                "name": "Anthony",
                "lastname": "Stark",
                "disabled": False,
                "created": str(date.today()),
                "is_superuser": False,
                "password": "ilovemark40"
            }
        }