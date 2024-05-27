from typing import Annotated

from fastapi import APIRouter, Form
from fastapi import Depends
from fastapi_limiter.depends import RateLimiter

from app.core.config import settings
from app.entity.game.user import User, UserResponse
from app.routers.core import BaseRouter, GameTag
from app.services.game.authenticate import AuthenticateService
from app.utils.jwt_service import JWTService


class AuthenticateRouter(BaseRouter):

    def __init__(self):
        self.tag = GameTag().get("Authenticate")

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix="/auth", tags=["Game > Authenticate"])

        @router.post("/login-for-docs",
                     dependencies=[
                         Depends(RateLimiter(times=settings.RATE_LIMIT_REQUEST, seconds=settings.RATE_LIMIT_TIME))])
        async def login_for_docs(
                username: int = Form(...),
        ):
            return {
                "access_token": JWTService().generate_token({'sub': username}),
                "": ""
            }

        @router.get("/me", response_model=UserResponse,
                    dependencies=[
                        Depends(RateLimiter(times=settings.RATE_LIMIT_REQUEST, seconds=settings.RATE_LIMIT_TIME))])
        async def read_users_me(
                current_user: Annotated[User, Depends(AuthenticateService().validate_token)],
        ):
            return current_user

        return router
