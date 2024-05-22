from app.routers.game.authenticate import AuthenticateRouter
from app.routers.game.root_character import RootCharacterRouter
from app.routers.game.user import UserRouter
from app.routers.core import BaseRouterGroup, BaseRouter


class GameRouterGroup(BaseRouterGroup):
    @property
    def sub_routers(self) -> list[BaseRouter]:
        return [
            AuthenticateRouter(),
            UserRouter(),
            RootCharacterRouter(),
        ]
