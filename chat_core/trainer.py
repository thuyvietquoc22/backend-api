import os
from typing import List

from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.base import BaseLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents.base import Document
from langchain_core.embeddings import Embeddings

from core.config import settings

embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)


class FAISSHelper:
    @staticmethod
    def create_db_from_files(loaders: list[BaseLoader], embeddings_model: Embeddings, character_name: str):
        documents: List[Document] = []
        for loader in loaders:
            documents.extend(loader.load())

        # Tách văn bản thành các đoạn nhỏ
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
        chunks = text_splitter.split_documents(documents)

        db = FAISS.from_documents(chunks, embeddings_model)

        db.save_local(f"models", index_name=character_name)

        return db

    @staticmethod
    def load_data(character_name: str, lang: str = "en"):
        return FAISS.load_local(f"models/{lang}", index_name=character_name, embeddings=embeddings,
                                allow_dangerous_deserialization=True)
