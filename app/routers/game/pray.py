from typing import Annotated

from fastapi import APIRouter, Depends

from app.entity.game.user import User
from app.exceptions.auth.authenticate_exception import AuthenticateException
from app.routers.core import BaseRouter, GameTag
from app.services.game.authenticate import AuthenticateService


class PrayRouter(BaseRouter):

    def __init__(self):
        self.tag = GameTag().get("Pray")

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix="/pray", tags=["Game > Pray"])

        @router.post("")
        async def pray(login_user: Annotated[User, Depends(AuthenticateService().validate_token)]):
            if login_user is None:
                raise AuthenticateException("Who are you ???")
            return {"message": f"{login_user.username} praying.", "status": "Not implemented yet."}

        return router
