from typing import Annotated

from fastapi import APIRouter, Depends

from app.entity.game.user import User
from app.routers.core import BaseRouter, GameTag
from app.services.game.authenticate import AuthenticateService
from app.services.game.character import CharacterService


class CharacterRouter(BaseRouter):

    def __init__(self):
        self.tags = GameTag().get("Character")
        self.character_service = CharacterService()

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix="/characters", tags=self.tags)

        @router.post("/{root_character_id}")
        def create_character_for_user(
                root_character_id: str,
                user: Annotated[User, Depends(AuthenticateService().get_logged_user)]):
            return self.character_service.create_character_for_user(user, root_character_id)

        return router
