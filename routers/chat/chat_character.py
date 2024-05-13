from fastapi import APIRouter

from core.contance import CharacterName
from routers.core import BaseRouter
from services.chat.chatbot import ChatbotService


class ChatCharacterRouter(BaseRouter):

    def __init__(self):
        self.chatbot_service = ChatbotService()

    @property
    def router(self) -> APIRouter:
        router = APIRouter(prefix="", tags=["Chat with Character"])

        @router.get("/")
        def get_character(message: str, user_id: int = 1):
            return self.chatbot_service.get_response(message, user_id)

        @router.post("/set_character")
        def set_character(character_name: CharacterName, user_id: int = 1):
            return self.chatbot_service.set_character_name(user_id, character_name)

        return router
