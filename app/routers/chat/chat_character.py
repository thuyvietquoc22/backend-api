from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from app.core.config import settings
from app.core.contance import CharacterName
from app.routers.core import BaseRouter
from app.services.chat.chatbot import ChatbotService


class ChatCharacterRouter(BaseRouter):

    def __init__(self):
        self.chatbot_service = ChatbotService()

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix="", tags=["Chat with Character"])

        @router.get("/",
                    dependencies=[
                        Depends(RateLimiter(times=settings.RATE_LIMIT_REQUEST, seconds=settings.RATE_LIMIT_TIME))])
        def get_character(message: str, user_id: int = 1):
            return self.chatbot_service.get_response(message, user_id)

        @router.post("/set_character",
                     dependencies=[
                         Depends(RateLimiter(times=settings.RATE_LIMIT_REQUEST, seconds=settings.RATE_LIMIT_TIME))])
        def set_character(character_name: CharacterName, user_id: int = 1):
            return self.chatbot_service.set_character_name(user_id, character_name)

        return router
