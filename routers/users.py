# Python
from typing import Union

# FastAPI
from fastapi import APIRouter, Path, Query, Body, Depends
from fastapi import HTTPException, status

# database
from database.mongo_client import MongoDB

# auth
from auth.auth import get_password_hash, get_current_user

# models
from models.user import BaseUser, User, UserDb

# util
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
    response_model = User,
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
    
    user = User(**user)

    return user


## get users or a user by username
@router.get(
    path = "/",
    status_code = status.HTTP_200_OK,
    response_model = Union[User, list],
    tags = ["Users"],
    summary = "Get a user or users"
)
async def get_users(
    username: Union[str, None] = Query(default=None)
):
    if not username:
        users = db_client.users_db.find().limit(25)
        users = [User(**user) for user in users]

        return users
    
    verify_username(username)

    user = db_client.users_db.find_one({"username": username})
    if not user:
        return None
    
    user = User(**user)

    return user


## get my info ##
@router.get(
    path = "/token/me",
    status_code = status.HTTP_200_OK,
    response_model = BaseUser,
    tags = ["Users"],
    summary = "Get my info"
)
async def read_users_me(
    current_user: BaseUser = Depends(get_current_user)
):
    return current_user


## register a user ##
@router.post(
    path = "/register",
    status_code = status.HTTP_201_CREATED,
    response_model = User,
    tags = ["Users"],
    summary = "Insert a user"
)
async def create_user(
    data: UserDb = Body(...)
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
    inserted_user = User(**inserted_user)

    return inserted_user


## get my info ##
@router.delete(
    path = "/",
    status_code = status.HTTP_202_ACCEPTED,
    response_model = BaseUser,
    tags = ["Users"],
    summary = "Delete my user info"
)
async def delete_user(
    current_user: BaseUser = Depends(get_current_user)
):
    verify_user_id(current_user.id)

    returned_data = db_client.users_db.update_one(
        filter = {"id": current_user.id},
        update = {"$set": {"disabled": True}}
    )
    if not returned_data.acknowledged:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = {
                "errmsg": "User not deleted"
            }
        )
    
    deleted_user = db_client.users_db.find_one({"id": current_user.id})
    deleted_user = BaseUser(**deleted_user)

    return deleted_user
