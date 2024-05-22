from pymongo import MongoClient

from app.core.config import settings

client = MongoClient(settings.MONGODB_URL)

ton_db = client["ton"]


def start_session():
    return client.start_session()
