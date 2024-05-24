from fastapi import APIRouter

from app.entity.game.root_character import RootCharacterCreate, RootCharacterUpdate
from app.routers.core import BaseRouter, GameTag
from app.services.game.root_character import RootCharacterService


class RootCharacterRouter(BaseRouter):

    def __init__(self):
        self.r_character_service = RootCharacterService()
        self.tags = GameTag().get("Root Character")

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix="/root-characters", tags=self.tags)

        @router.get("")
        def get_characters():
            return self.r_character_service.get_root_characters()

        @router.get("/{character_id}")
        def get_character(character_id: int):
            return self.r_character_service.get_root_character_by_id(character_id)

        @router.post("")
        def create_root_character(root_character: RootCharacterCreate):
            return self.r_character_service.create_root_character(root_character)

        @router.put("/{root_character_id}")
        def update_root_character(
                root_character_id: str,
                root_character: RootCharacterUpdate):
            return self.r_character_service.update_root_character(root_character_id, root_character)

        return router
