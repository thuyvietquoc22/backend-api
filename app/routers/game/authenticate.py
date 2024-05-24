from typing import Annotated

from fastapi import APIRouter, Form
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

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

        @router.post("/login-for-docs")
        async def login_for_docs(
                username: int = Form(...),
        ):
            return {
                "access_token": JWTService().generate_token({'sub': username}),
                "": ""
            }

        @router.get("/me", response_model=UserResponse)
        async def read_users_me(
                current_user: Annotated[User, Depends(AuthenticateService().validate_token)],
        ):
            return current_user

        return router
