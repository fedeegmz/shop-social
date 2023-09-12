# FastAPI
from fastapi import FastAPI

# routers
from routers import carts, users, token, shops, products


app = FastAPI()
app.include_router(users.router)
app.include_router(shops.router)
app.include_router(token.router)
app.include_router(products.router)
app.include_router(carts.router)


@app.get(
    path = "/",
    include_in_schema = False
)
async def root():
    return {"Hello": "World"}