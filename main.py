# FastAPI
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter

# Redis
import redis

# security
from security.config import settings

# routers
from routers import users, token, shops, products, carts


app = FastAPI()
app.include_router(users.router)
app.include_router(token.router)
app.include_router(shops.router)
app.include_router(products.router)
app.include_router(carts.router)


@app.on_event("startup")
async def startup():
    r = redis.Redis(
        host = settings.redis_limiter_host,
        port = settings.redis_limiter_port,
        password = settings.redis_limiter_password
    )
    await FastAPILimiter.init(r)

@app.on_event("shutdown")
async def shutdown():
    await FastAPILimiter.close()


@app.get(
    path = "/",
    include_in_schema = False
)
async def root():
    return {"Hello": "World"}