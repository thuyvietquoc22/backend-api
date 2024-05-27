from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from app.core.config import settings
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

        @router.get("",
                    dependencies=[
                        Depends(RateLimiter(times=settings.RATE_LIMIT_REQUEST, seconds=settings.RATE_LIMIT_TIME))])
        def get_characters():
            return self.r_character_service.get_root_characters()

        @router.get("/{character_id}",
                    dependencies=[
                        Depends(RateLimiter(times=settings.RATE_LIMIT_REQUEST, seconds=settings.RATE_LIMIT_TIME))])
        def get_character(character_id: int):
            return self.r_character_service.get_root_character_by_id(character_id)

        @router.post("",
                     dependencies=[
                         Depends(RateLimiter(times=settings.RATE_LIMIT_REQUEST, seconds=settings.RATE_LIMIT_TIME))])
        def create_root_character(root_character: RootCharacterCreate):
            return self.r_character_service.create_root_character(root_character)

        @router.put("/{root_character_id}",
                    dependencies=[
                        Depends(RateLimiter(times=settings.RATE_LIMIT_REQUEST, seconds=settings.RATE_LIMIT_TIME))])
        def update_root_character(
                root_character_id: str,
                root_character: RootCharacterUpdate):
            return self.r_character_service.update_root_character(root_character_id, root_character)

        return router
