from fastapi import APIRouter

from entity.user import UserRegister
from routers.core import BaseRouter
from services.auth.user import UserService


class UserRouter(BaseRouter):

    def __init__(self):
        self.user_service = UserService()

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix="/user", tags=["Authenticate > Users"])

        @router.post("")
        def register_user(user_register: UserRegister):
            return self.user_service.register_user(user_register)

        @router.get("")
        def get_user_info_by_token(token: str):
            return self.user_service.get_user_info_by_token(token)

        @router.get("/{tele_id}")
        def get_user(tele_id: str):
            return self.user_service.get_user_info_by_id(tele_id)

        @router.get("/invited/{tele_id}")
        def get_invited_user(tele_id: int):
            invited_user = self.user_service.get_invited_user(tele_id)
            return len(invited_user)

        @router.get("/token/{tele_id}")
        def get_user_token(tele_id: int):
            return self.user_service.get_user_token(tele_id)

        return router
