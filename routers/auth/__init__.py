from routers.auth.user import UserRouter
from routers.core import BaseRouterGroup, BaseRouter


class AuthRouterGroup(BaseRouterGroup):
    @property
    def sub_routers(self) -> list[BaseRouter]:
        return [
            UserRouter()
        ]
