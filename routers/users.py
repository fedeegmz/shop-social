# Python
from typing import Union

# FastAPI
from fastapi import APIRouter, Path, Query, Body, Depends
from fastapi import HTTPException, status

# database
from database.mongo_client import MongoDB

# models
from models.user import User, UserDb, UserIn

# util
from util.auth import get_password_hash, get_current_user
from util.verify import verify_username, verify_user_id
from util.white_lists import get_white_list_usernames


db_client = MongoDB()

router = APIRouter(
    prefix = "/users"
)


### PATH OPERATIONS ###

## get user by id ##
@router.get(
    path = "/{id}",
    status_code = status.HTTP_200_OK,
    response_model = UserDb,
    tags = ["Users"],
    summary = "Get a user by ID"
)
async def get_user(
    id: str = Path(...)
):
    verify_user_id(id)

    user = db_client.users_db.find_one({"id": id})
    if not user:
        return None
    
    user = UserDb(**user)

    return user


## get users or a user by username
@router.get(
    path = "/",
    status_code = status.HTTP_200_OK,
    # response_model = Union[UserDb, list],
    tags = ["Users"],
    summary = "Get a user or users"
)
async def get_users(
    username: Union[str, None] = Query(default=None)
):
    if not username:
        users = db_client.users_db.find().limit(25)
        users = [UserDb(**user) for user in users]

        return users
    
    verify_username(username)

    user = db_client.users_db.find_one({"username": username})
    if not user:
        return None
    
    user = UserDb(**user)

    return user


## get my info ##
@router.get(
    path = "/users/me",
    status_code = status.HTTP_200_OK,
    response_model = User,
    tags = ["Users"],
    summary = "Get my info"
)
async def read_users_me(
    current_user: User = Depends(get_current_user)
):
    return current_user


## register a user ##
@router.post(
    path = "/register",
    status_code = status.HTTP_201_CREATED,
    response_model = UserDb,
    tags = ["Users"],
    summary = "Insert a user"
)
async def create_user(
    data: UserIn = Body(...)
):  
    if data.username in get_white_list_usernames():
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = {
                "errmsg": "Username exists"
            }
        )
    
    data.password = get_password_hash(data.password)
    returned_data = db_client.users_db.insert_one(data.dict())
    if not returned_data.acknowledged:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = {
                "errmsg": "User not inserted"
            }
        )
    
    inserted_user = db_client.users_db.find_one({"id": data.id})
    inserted_user = UserDb(**inserted_user)

    return inserted_user
