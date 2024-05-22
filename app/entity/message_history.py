from typing import List

from openai.types.chat import ChatCompletionUserMessageParam, ChatCompletionAssistantMessageParam, \
    ChatCompletionMessageParam
from pydantic import BaseModel

from app.core.contance import CharacterName


class MessageHistory(BaseModel):
    user_id: int
    user_message: List[ChatCompletionUserMessageParam] = []
    assistant_message: List[ChatCompletionAssistantMessageParam] = []
    character_name: CharacterName = None

    @property
    def chat_list(self) -> List[ChatCompletionMessageParam]:
        user_message_count = len(self.user_message)
        assistant_message_count = len(self.assistant_message)
        min_index = max(user_message_count, assistant_message_count)

        chat_list: List[ChatCompletionMessageParam] = []

        for i in range(min_index):
            try:
                chat_list.append(self.user_message[i])
            except IndexError:
                pass
            try:
                chat_list.append(self.assistant_message[i])
            except IndexError:
                pass

        return chat_list

    def add_user_message(self, message: str):
        new_message = ChatCompletionUserMessageParam(role="user", content=message)
        self.user_message = (self.user_message + [new_message])[-9:]

    def add_assistant_message(self, message: str):
        new_message = ChatCompletionAssistantMessageParam(role="assistant", content=message)
        self.assistant_message = (self.assistant_message + [new_message])[-9:]

    def clear_message_history(self):
        self.user_message = []
        self.assistant_message = []
        return True
