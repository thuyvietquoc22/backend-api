from app.routers.core import BaseRouterGroup, BaseRouter
from app.routers.game.authenticate import AuthenticateRouter
from app.routers.game.battle import BattleRouter
from app.routers.game.character import CharacterRouter
from app.routers.game.pray import PrayRouter
from app.routers.game.root_character import RootCharacterRouter
from app.routers.game.user import UserRouter


class GameRouterGroup(BaseRouterGroup):
    @property
    def sub_routers(self) -> list[BaseRouter]:
        return [
            AuthenticateRouter(),
            UserRouter(),
            RootCharacterRouter(),
            PrayRouter(),
            CharacterRouter(),
            BattleRouter()
        ]
