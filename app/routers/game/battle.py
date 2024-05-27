from typing import Annotated

from fastapi import APIRouter, Depends

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
        def start_battle(character_id: str, user: Annotated[User, Depends(AuthenticateService().get_logged_user)]):
            return self.battle_service.generate_bot(character_id, user)

        @router.post("/end")
        def end_battle():
            pass

        return router
