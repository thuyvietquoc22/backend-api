from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import JWTDecodeError

from app.entity.user import User, UserResponse
from app.routers.core import BaseRouter, GameTag
from app.services.game.authenticate import AuthenticateService
from app.services.game.user import UserService
from app.utils.jwt_service import JWTService


class AuthenticateRouter(BaseRouter):

    def __init__(self):
        self.tag = GameTag().get("Authenticate")

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix="/authenticate", tags=["Game > Authenticate"])

        @router.get("/me", response_model=UserResponse)
        async def read_users_me(
                current_user: Annotated[User, Depends(AuthenticateService().validate_token)],
        ):
            return current_user

        return router
