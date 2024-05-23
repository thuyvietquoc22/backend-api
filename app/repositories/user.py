from pymongo.collection import Collection

from app.db.mongo.auth.user import user_collection
from app.decorator.parser import parse_as
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
