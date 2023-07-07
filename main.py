# FastAPI
from fastapi import FastAPI

# routers
from routers import users, token, shops


app = FastAPI()
app.include_router(users.router)
app.include_router(shops.router)
app.include_router(token.router)


@app.get("/")
async def root():
    return {"Hello": "World"}