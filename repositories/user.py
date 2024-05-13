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
            {'ref_code': ref_code},
        )
