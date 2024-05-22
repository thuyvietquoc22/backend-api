from loguru import logger
from openai import OpenAI
from openai.types.chat import ChatCompletion

from app.core.config import settings
from app.core.contance import CharacterName
from app.decorator import singleton
from app.entity.message_history import MessageHistory
from app.services.chat.faiss_service import FAISSService
from app.services.chat.message_tracking import MessageTrackingService


@singleton
class ChatbotService:

    def __init__(self):
        self.message_tracking_service = MessageTrackingService()
        self.faiss_service = FAISSService()

    def get_response(self, message, user_id):

        message_history = self.message_tracking_service.get_message_history(user_id)

        response = self.generate_response_chat(message_history, message)
        self.message_tracking_service.add_assistant_message(user_id, response)
        return response

    def generate_response_chat(self, message_list: MessageHistory, message: str):
        character_name = message_list.character_name or CharacterName.AZUSA_NAKANO
        faiss_index = self.faiss_service.get_index(character_name.character_name)
        system_prompt = ""

        message_list.add_user_message(message)
        if faiss_index is not None:
            try:
                docs = faiss_index.similarity_search(query=message, k=2)

                for doc in docs:
                    system_prompt += doc.page_content + "\n\n"
            except Exception as e:
                logger.error(f"Error when load document: {e}")
        else:
            logger.error("Index not found")

        return self.open_ai_response(message_list, system_prompt)

    def open_ai_response(self, message_history: MessageHistory, system_message: str,
                         open_ai_model_name="gpt-3.5-turbo"):
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        system_message = system_message + "\n\n" + settings.SYSTEM_PROMPT

        message = [
                      {
                          "role": "system",
                          "content": system_message
                      },
                  ] + message_history.chat_list

        response: ChatCompletion = client.chat.completions.create(
            model=open_ai_model_name,
            temperature=0,
            messages=message
        )

        assistant_response = response.choices[0].message.content

        return assistant_response

    def set_character_name(self, user_id, character_name):
        return self.message_tracking_service.set_character_name(user_id, character_name)
