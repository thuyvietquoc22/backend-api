from pymongo.collection import Collection

from app.db.mongo.game.character import character_collection
from app.repositories.core import BaseRepository


class CharacterRepository(BaseRepository):
    @property
    def collection(self) -> Collection:
        return character_collection
