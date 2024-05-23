from bson import ObjectId
from pymongo.collection import Collection

from app.db.mongo.auth.user import user_collection
from app.decorator.parser import parse_as
from app.entity.game.stone import Stone
from app.entity.game.user import UserResponse, User
from app.repositories.core import BaseRepository


class UserRepository(BaseRepository):
    @property
    def collection(self) -> Collection:
        return user_collection

    @parse_as(UserResponse, get_first=True)
    def check_ref_code(self, ref_code):
        return self.aggregate(
            {"$match": {'tele_id': ref_code}},
        )

    @parse_as(User, get_first=True, exception_when_none=True, message_exception="User not found")
    def get_user_info_by_tele_id(self, tele_id):
        return self.aggregate(
            {"$match": {'tele_id': tele_id}},
        )

    @parse_as(list[UserResponse])
    def get_invited_user(self, tele_id):
        return self.aggregate(
            {"$match": {'ref_code': tele_id}},
        )

    def update_bag(self, stones: list[Stone], inserted_index: list[int], old_len: int, owner_id: str):
        inserted_ = {}
        update_amount = {
            f"stones.{index}.amount": stone.amount
            for index, stone in enumerate(stones)
            if index < old_len and index in inserted_index
        }
        inserted_.update({"$set": update_amount})

        update_inserted = [stone.dict() for index, stone in enumerate(stones) if index >= old_len]
        if len(update_inserted):
            inserted_.update({"$push": {"stones": {"$each": update_inserted}}})

        self.collection.update_one(
            {"_id": ObjectId(owner_id)},
            inserted_
        )
