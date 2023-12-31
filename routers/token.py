# FastAPI
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

# security
from security.auth import create_access_token, authenticate_user

# models
from models.token import Token


ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter(
    prefix = "/login",
    # responses={status.HTTP_404_NOT_FOUND: {"error": "Not Found"}}
)


### PATH OPERATIONS ###

@router.post(
    path = "/token",
    status_code = status.HTTP_202_ACCEPTED,
    response_model = Token,
    summary = "Login a user",
    tags = ["Token"]
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            headers = {"WWW-Authenticate": "Bearer"},
            detail = {
                "errmsg": "Incorrect username or password"
            }
        )
    
    access_token = create_access_token(
        data = {"sub": user.username},
        expires_delta = ACCESS_TOKEN_EXPIRE_MINUTES
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

