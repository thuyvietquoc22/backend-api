from core.contance import CharacterName
from decorator import singleton
from entity.message_history import MessageHistory


@singleton
class MessageTrackingService:
    def __init__(self):
        self.message_repository: list[MessageHistory] = []

    def get_message_history(self, user_id):
        return self._get_message_history(user_id)

    def _get_message_history(self, user_id) -> MessageHistory:
        result = next((message for message in self.message_repository if message.user_id == user_id), None)
        if result is not None:
            return result
        else:
            result = MessageHistory(user_id=user_id)
            self.message_repository.append(result)
            return result

    def add_user_message(self, user_id, message):
        message_history: MessageHistory = self._get_message_history(user_id)
        if message_history:
            message_history.user_message.append(message)
        else:
            self.message_repository.append(MessageHistory(user_id=user_id, messages=[message]))

    def add_assistant_message(self, user_id, message):
        message_history = self._get_message_history(user_id)
        if message_history:
            message_history.add_assistant_message(message)
        else:
            message_history = MessageHistory(user_id=user_id)
            message_history.add_assistant_message(message)
            self.message_repository.append(message_history)
        return True

    def clear_message_history(self, user_id):
        old_size = len(self.message_repository)
        self.message_repository = [message for message in self.message_repository if message.user_id != user_id]
        return len(self.message_repository) < old_size

    def clear_all_message_history(self):
        self.message_repository = []
        return True

    def set_character_name(self, user_id: int, character_name: CharacterName):
        message_history = self._get_message_history(user_id)
        if message_history:
            message_history.character_name = character_name
        else:
            self.message_repository.append(MessageHistory(user_id=user_id, character_name=character_name))
        return True
