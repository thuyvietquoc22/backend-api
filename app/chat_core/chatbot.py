# from typing import Iterable
#
# from loguru import logger
# from openai import OpenAI
# from openai.types.chat import ChatCompletion, ChatCompletionMessageParam
#
# from chat_core.trainer import FAISSHelper
# from core.config import settings
#
# train_data = [
#     {
#         "glob": "Azusa Nakano.pdf",
#         "character_name": "azura_nakano"
#     },
#     {
#         "glob": "edge runner lucy.pdf",
#         "character_name": "edge_runner_lucy"
#     },
#     {
#         "glob": "Sakura.pdf",
#         "character_name": "sakura"
#     },
# ]
#
# faiss_indexes = {i['character_name']: FAISSHelper.load_data(i['character_name']) for i in train_data}
#
#
# def generate_response_chat(message_list: Iterable[ChatCompletionMessageParam], character_name=None):
#     faiss_index = faiss_indexes.get(character_name, None)
#     system_prompt = ""
#     if faiss_index is not None:
#         # Add extra text to the content of the last message
#         last_message = message_list[-1]
#
#         # Get the most similar documents to the last message
#         try:
#             docs = faiss_index.similarity_search(query=last_message["content"], k=2)
#
#             for doc in docs:
#                 system_prompt += doc.page_content + "\n\n"
#         except Exception as e:
#             # print(f"Error while fetching : {e}")
#             logger.error(f"Error while fetching : {e}")
#     else:
#         logger.error("Index not found")
#     client = OpenAI(api_key=settings.OPENAI_API_KEY)
#     response: ChatCompletion = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         temperature=0,
#         messages=[
#                      {"role": "system",
#                       "content": system_prompt + "\n\n" + settings.SYSTEM_PROMPT},
#                  ] + message_list
#     )
#
#     assistant_response = response.choices[0].message.content
#
#     return assistant_response
