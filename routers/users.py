# FastAPI
from fastapi import APIRouter, Path, Body
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

# database
from database.mongo_client import db_client

# models
from models.user import User, UserDb

# util
from util.auth import get_password_hash
from util.verify import verify_username


router = APIRouter(
    prefix = "/users"
)


@router.get(
    path = "/",
    status_code = status.HTTP_200_OK,
    tags = ["users"],
    summary = "Get all users"
)
async def get_users():
    users = db_client.users_db.find(
        {},
        {
            "username": 1,
            "name": 1,
            "lastname": 1
        }
    )
    
    return [
        {
            "username": user["username"],
            "name": user["name"],
            "lastname": user["lastname"],
        } for user in users]

@router.get(
    path = "/{username}",
    status_code = status.HTTP_200_OK,
    tags = ["users"],
    summary = "Get a user"
)
async def get_user(
    username: str = Path(...)
):
    verify_username(username)

    user = db_client.users_db.find_one({"username": username})
    if not user:
        return None
    user = User(**user)
    del user.password

    return user

@router.post(
    path = "/signup",
    status_code = status.HTTP_201_CREATED,
    tags = ["users"],
    summary = "Insert a user"
)
async def create_user(
    data: User = Body(...)
):
    if not isinstance(data, User):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = {
                "errmsg": "Incorrect user",
                "errdetail": str(err)
            }
        )
    
    try:
        # TODO: verificar que el username no se repite
        user = UserDb(**data.dict())
        user.password = get_password_hash(user.password)
        inserted_id = db_client.users_db.insert_one(user.dict())

    except Exception as err:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = {
                "errmsg": "User not inserted",
                "errdetail": str(err)
            }
        )
    return data.dict()