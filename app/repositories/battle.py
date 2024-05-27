from bson import ObjectId
from pymongo.collection import Collection

from app.db.mongo.game.battle import battle_collection
from app.decorator.parser import parse_as
from app.entity.game.battle import BattleResponse
from app.repositories.core import BaseRepository


class BattleRepository(BaseRepository):
    @property
    def collection(self) -> Collection:
        return battle_collection

    @property
    def root_pipeline(self):
        return [
            {'$lookup': {'from': 'users', 'localField': 'user_id', 'foreignField': '_id', 'as': 'user'}},
            {'$lookup': {'from': 'character', 'localField': 'character_id', 'foreignField': '_id', 'as': 'character'}},
            {'$unwind': '$character'},
            {'$unwind': '$user'},
        ]

    @parse_as(list[BattleResponse])
    def find_battling_by_user_id(self, user_id: str):
        return self.aggregate(
            {"$match": {"user_id": ObjectId(user_id), "battling": True}},
        )

    def end_battle(self, battle_id, battle_end):
        self.collection.update_one(
            {"_id": ObjectId(battle_id)},
            {"$set": {
                "battling": False,
                "remaining_hp": battle_end.user_hp,
                "bot_info.remaining_hp": battle_end.bot_hp,
            }})

        return self.get_by_id(battle_id)

    def find_all_battle(self, id):
        return self.aggregate(
            {"$match": {"user_id": ObjectId(id)}},
            {"$sort": {"_id": -1}},
        )
