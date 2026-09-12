import time
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from app.core.redis_server import redis_client

RATE_LIMIT = 5
WINDOW = 60


async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host

    current_time = int(time.time() / WINDOW)

    key = f"rate_limit:{client_ip}:{current_time}"

    count = redis_client.incr(key)
    print("Client IP:", client_ip)
    print("Hitting URL:", request.url.path)
    print("Request Count:", count)


    if count == 1:
        redis_client.expire(key, WINDOW)

    if count > RATE_LIMIT:
        return JSONResponse(status_code=429, content={"detail": "Too Many Request"})
    
    response = await call_next(request)

    return response
