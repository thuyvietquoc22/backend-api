import aioredis
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from loguru import logger


def register_event(app: FastAPI):
    # limiter = Limiter(key_func=get_remote_address)
    # app.state.limiter = limiter
    # app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    @app.on_event("startup")
    async def startup_event():
        try:
            redis = await aioredis.create_redis_pool("redis://localhost")
            await FastAPILimiter.init(redis)
            logger.info("FastAPILimiter initialized")
        except Exception as e:
            logger.error(e)

    @app.on_event("shutdown")
    async def shutdown_event():
        try:
            logger.info("FastAPILimiter closing...")
            await FastAPILimiter.close()
        except Exception as e:
            logger.error(e)
    # return limiter
