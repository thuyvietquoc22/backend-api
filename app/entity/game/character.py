from bson import ObjectId

from app.entity.core import BaseMongoModel, PyObjectId
from app.entity.game.root_character import CharacterAttribute, RootCharacter
from app.utils.generate_code import generate_random_code
from pydantic import field_serializer


class BaseCharacter(BaseMongoModel, CharacterAttribute):
    owner_id: str
    code: str
    root_character_id: PyObjectId


class CharacterCreate(BaseCharacter):

    @classmethod
    def from_root_character(cls, root_character: RootCharacter, owner_id: str):
        return cls(
            owner_id=owner_id,
            **root_character.dict(),
            code=generate_random_code(),
            root_character_id=root_character.id
        )

    @staticmethod
    @field_serializer("root_character_id", "owner_id")
    def serialize_id(value):
        return ObjectId(value)
