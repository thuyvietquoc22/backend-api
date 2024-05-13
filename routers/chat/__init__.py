from routers.chat.chat_character import ChatCharacterRouter
from routers.core import BaseRouter, BaseRouterGroup


class ChatRouterGroup(BaseRouterGroup):

    @property
    def prefix(self) -> str:
        return "/chat"

    @property
    def sub_routers(self) -> list[BaseRouter]:
        return [
            ChatCharacterRouter(),
        ]
