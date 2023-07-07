from datetime import date
from pydantic import BaseModel, Field


class UserLogin(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

class User(UserLogin):
    name: str = Field(...)
    lastname: str = Field(...)

class UserDb(User):
    disabled: bool = Field(default=False)
    created: str = Field(default=str(date.today()))
    is_superuser: bool = Field(default=False)