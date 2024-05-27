from pymongo.collection import Collection

from app.db.mongo.game.root_character import root_character_collection
from app.repositories.core import BaseRepository


class RootCharacterRepository(BaseRepository):
    @property
    def collection(self) -> Collection:
        return root_character_collection
