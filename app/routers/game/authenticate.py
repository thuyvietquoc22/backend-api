from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends

from app.entity.game.user import User, UserResponse
from app.routers.core import BaseRouter, GameTag
from app.services.game.authenticate import AuthenticateService


class AuthenticateRouter(BaseRouter):

    def __init__(self):
        self.tag = GameTag().get("Authenticate")

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix="/auth", tags=["Game > Authenticate"])

        @router.get("/me", response_model=UserResponse)
        async def read_users_me(
                current_user: Annotated[User, Depends(AuthenticateService().validate_token)],
        ):
            return current_user

        return router
