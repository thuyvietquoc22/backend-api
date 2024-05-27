from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from app.core.config import settings
from app.entity.game.user import User
from app.exceptions.auth.authenticate_exception import AuthenticateException
from app.routers.core import BaseRouter, GameTag
from app.services.game.authenticate import AuthenticateService
from app.services.game.pray import PrayService


class PrayRouter(BaseRouter):

    def __init__(self):
        self.pray_service = PrayService()
        self.tag = GameTag().get("Pray")

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix="/pray", tags=["Game > Pray"])

        @router.post("",
                     dependencies=[
                         Depends(RateLimiter(times=settings.RATE_LIMIT_REQUEST, seconds=settings.RATE_LIMIT_TIME))])
        async def pray(login_user: Annotated[User, Depends(AuthenticateService().validate_token)]):
            if login_user is None:
                raise AuthenticateException("Who are you ???")
            return self.pray_service.pray(login_user)

        return router
