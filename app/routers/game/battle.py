from typing import Annotated

from fastapi import APIRouter, Depends

from app.entity.game.battle import BattleStart, BattleEnd
from app.entity.game.user import User
from app.routers.core import BaseRouter, GameTag
from app.services.game.authenticate import AuthenticateService
from app.services.game.battle import BattleService


class BattleRouter(BaseRouter):

    def __init__(self):
        self.tags = GameTag().get("Battle")
        self.battle_service = BattleService()

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix="/battles", tags=self.tags)

        @router.post("/generate-bot/{character_id}")
        def random_bot_by_character_id(character_id: str,
                                       user: Annotated[User, Depends(AuthenticateService().get_logged_user)]):
            return self.battle_service.generate_bot(character_id, user)

        @router.post("/start")
        def start_battle(battle_create: BattleStart,
                         user: Annotated[User, Depends(AuthenticateService().get_logged_user)]):
            return self.battle_service.start_battle(battle_create, user)

        @router.post("/end/{battle_id}")
        def end_battle(
                battle_id: str,
                battle_end: BattleEnd,
                user: Annotated[User, Depends(AuthenticateService().get_logged_user)]
        ):
            return self.battle_service.end_battle(battle_id, battle_end, user)

        @router.get("/history")
        def get_battle_history(user: Annotated[User, Depends(AuthenticateService().get_logged_user)]):
            return self.battle_service.get_battle_history(user)

        return router
