from bson import ObjectId
from pydantic import Field, BaseModel, field_serializer

from app.entity.core import BaseMongoModel, PyObjectId
from app.entity.game.bot import BotInfo
from app.entity.game.character import CharacterResponse
from app.entity.game.user import UserInfo


class BattleStart(BaseModel):
    character_id: PyObjectId = Field(exclude=True)
    bot_info: BotInfo


class BattleEnd(BaseModel):
    bot_hp: int
    user_hp: int


class BaseBattle(BaseMongoModel):
    bot_info: BotInfo
    remaining_hp: int = Field(default=100, ge=0, le=100)
    battling: bool = False

    @property
    def is_win(self):
        return self.remaining_hp > self.bot_info.remaining_hp


class BattleCreate(BaseBattle):
    user_id: PyObjectId
    character_id: PyObjectId

    @classmethod
    def from_battle_start(cls, battle_start: BattleStart, user_id: ObjectId):
        return cls(
            user_id=user_id,
            character_id=battle_start.character_id,
            bot_info=battle_start.bot_info,
            battling=True,
            remaining_hp=100
        )

    @field_serializer("user_id", "character_id")
    def serialize_id(self, value):
        return ObjectId(value)


class BattleResponse(BaseBattle):
    user: UserInfo
    character: CharacterResponse
