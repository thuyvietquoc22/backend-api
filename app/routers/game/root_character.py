from fastapi import APIRouter

from app.routers.core import BaseRouter


class RootCharacterRouter(BaseRouter):

    def __init__(self):
        pass

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix="/root-characters", tags=["Game > Character"])

        @router.get("")
        def get_characters():
            return "Get characters"

        @router.get("/{character_id}")
        def get_character(character_id: int):
            return "Get character"

        @router.post("")
        def create_root_character():
            return "Create character"

        @router.put("")
        def update_root_character():
            return "Update character"

        return router
