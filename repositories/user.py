from pymongo.collection import Collection

from db.mongo.auth.user import user_collection
from decorator.parser import parse_as
from entity.user import UserResponse
from repositories.core import BaseRepository


class UserRepository(BaseRepository):
    @property
    def collection(self) -> Collection:
        return user_collection

    @parse_as(UserResponse, get_first=True)
    def check_ref_code(self, ref_code):
        return self.aggregate(
            {"$match": {'tele_id': ref_code}},
        )

    @parse_as(UserResponse, get_first=True)
    def get_user_info_by_tele_id(self, tele_id):
        return self.aggregate(
            {"$match": {'tele_id': tele_id}},
        )

    @parse_as(list[UserResponse])
    def get_invited_user(self, tele_id):
        return self.aggregate(
            {"$match": {'ref_code': tele_id}},
        )
