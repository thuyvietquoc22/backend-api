from abc import ABC
from typing import Optional

from pydantic import BaseModel

from app.entity.core import BaseMongoModel
from app.entity.game.stone import StoneColor


class CharacterAttribute(BaseModel):
    """Các thuộc tính của nhân vật"""
    attack: int
    defense: int
    energy: int

    # TODO: Add MORE attrs for Character

    def get_current_stats(self, stone_color: StoneColor) -> int | None:
        if stone_color == "red":
            return self.attack

        if stone_color == "green":
            return self.defense

        if stone_color == "blue":
            return self.energy

        return None


class BaseRootCharacter(BaseMongoModel, ABC):
    """Các thuộc tính cơ bản ban đầu của nhân vật gốc"""
    url_model: str
    name: str


class RootCharacter(BaseRootCharacter, CharacterAttribute):
    """Nhân vật gốc chứa thông tin cơ bản và thuộc tính của nhân vật"""
    pass


class RootCharacterUpdate(BaseModel):
    url_model: Optional[str] = None
    name: Optional[str] = None
    attack: Optional[int] = None
    defense: Optional[int] = None
    energy: Optional[int] = None


class RootCharacterCreate(RootCharacter):
    pass
