from fastapi_limiter import FastAPILimiter

# limiter = FastAPILimiter(
#     key_func = lambda request: request.client.host,
#     default_limits = ["5 per minute"]
# )
limiter = FastAPILimiter()