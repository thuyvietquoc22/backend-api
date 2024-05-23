from abc import ABC

from pydantic import BaseModel

from app.entity.core import BaseMongoModel


class CharacterAttribute(BaseModel):
    """Các thuộc tính của nhân vật"""
    attack: int
    defense: int
    energy: int
    # TODO: Add MORE attrs for Character


class BaseRootCharacter(BaseMongoModel, ABC):
    """Các thuộc tính cơ bản ban đầu của nhân vật gốc"""
    url_model: str
    name: str


class RootCharacter(BaseRootCharacter, CharacterAttribute):
    """Nhân vật gốc chứa thông tin cơ bản và thuộc tính của nhân vật"""
    pass


class RootCharacterCreate(BaseRootCharacter):
    pass
