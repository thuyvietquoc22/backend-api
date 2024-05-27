from typing import Annotated

from fastapi import APIRouter, Depends

from app.entity.game.user import UserRegister, UserBasicResponse, User
from app.routers.core import BaseRouter, GameTag
from app.services.game.authenticate import AuthenticateService
from app.services.game.user import UserService


class UserRouter(BaseRouter):

    def __init__(self):
        self.user_service = UserService()
        self.tag = GameTag().get("User info")

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix="/users", tags=self.tag)

        @router.post("")
        def register_user(user_register: UserRegister):
            return self.user_service.register_user(user_register)

        @router.get("")
        def get_user_info_by_token(token: str):
            return self.user_service.get_user_info_by_token(token)

        @router.get("/bag")
        def get_user_bag(user: Annotated[User, Depends(AuthenticateService().get_logged_user)]):
            return user.stones

        @router.get("/experience")
        def get_user_exp(user: Annotated[User, Depends(AuthenticateService().get_logged_user)]):
            return user.exp

        @router.get("/{tele_id}", response_model=UserBasicResponse)
        def get_user(tele_id: int):
            return self.user_service.get_user_info_by_id(tele_id)

        @router.get("/count-invited/{tele_id}")
        def get_invited_user(tele_id: int):
            invited_user = self.user_service.get_invited_user(tele_id)
            return len(invited_user)

        @router.get("/token/{tele_id}")
        def generate_token_for_user(tele_id: int):
            return self.user_service.get_user_token(tele_id)

        return router
