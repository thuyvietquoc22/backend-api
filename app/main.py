from contextlib import asynccontextmanager
from math import ceil

import redis.asyncio as redis
import uvicorn
from fastapi import FastAPI, Request, Response, HTTPException, status
from fastapi_limiter import FastAPILimiter

from app.core.config import settings
from app.exceptions.exception_handler import register_exception_handler
from app.middlewares import register_middlewares
from app.routers.router import register_router


async def service_name_identifier(request: Request):
    service = request.headers.get("Service-Name")
    return service


async def custom_callback(request: Request, response: Response, expire: int):
    """
    default callback when too many requests
    :param request:
    :param expire: The remaining milliseconds
    :param response:
    :return:
    """
    expire = ceil(expire / 1000)

    raise HTTPException(
        status.HTTP_429_TOO_MANY_REQUESTS,
        f"Too Many Requests. Retry after {expire} seconds.",
        headers={"Retry-After": str(expire)},
    )


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis_connection = redis.from_url(settings.REDIS_URL, encoding="utf8")
    await FastAPILimiter.init(
        redis=redis_connection,
        prefix=settings.REDIS_PREFIX,
        identifier=service_name_identifier,
        http_callback=custom_callback,
    )
    yield
    await FastAPILimiter.close()


app = FastAPI(
    lifespan=lifespan,
    swagger_ui_parameters={
        "tagsSorter": "alpha",
    }
)

# db = initialize_db()
# generate_table(db)
# register_event(app)
register_exception_handler(app)
register_middlewares(app)
register_router(app)
#
# # Approach #1: Create global variable for redis
# global_cache = redis.Redis(
#     host=os.environ.get('REDIS_HOST', 'localhost'),
#     port=os.environ.get('REDIS_PORT', 6379),
#     db=os.environ.get('REDIS_DB', 0),
#     decode_responses=True
# )

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
