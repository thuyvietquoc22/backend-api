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

        return router
