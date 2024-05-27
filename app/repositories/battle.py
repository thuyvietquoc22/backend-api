from pymongo.collection import Collection

from app.db.mongo.game.battle import battle_collection
from app.repositories.core import BaseRepository


class BattleRepository(BaseRepository):
    @property
    def collection(self) -> Collection:
        return battle_collection
