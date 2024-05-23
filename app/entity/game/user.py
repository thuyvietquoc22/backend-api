from typing import Optional, Any

from pydantic import BaseModel, field_validator

from app.entity.core import BaseMongoModel
from app.entity.game.stone import Stone
from app.utils.jwt_service import JWTSerializer


class BaseUser(BaseMongoModel, JWTSerializer):
    tele_id: int
    username: Optional[str] = None
    full_name: Optional[str] = None
    photo_url: Optional[str] = None
    ref_code: Optional[int] = None
    experience: Optional[int] = 0
    stones: list[Stone] = []

    @field_validator("stones")
    def validate_stones(cls, value):
        if value is None:
            return []

        if len(value) != len(set(value)):
            raise ValueError("Duplicate stones")

        return value

    @property
    def to_encode(self) -> dict[str, Any]:
        return {
            "sub": self.tele_id,
        }


class UserRegister(BaseModel):
    tele_id: int
    username: Optional[str] = None
    full_name: Optional[str] = None
    photo_url: Optional[str] = None
    ref_code: Optional[int] = None
    mnemonic: Optional[str] = None


class UserCreate(BaseUser):
    mnemonic: Optional[str] = None

    @classmethod
    def from_register(cls, register: UserRegister):
        return cls(
            tele_id=register.tele_id,
            user_name=register.username,
            full_name=register.full_name,
            photo_url=register.photo_url,
            ref_code=register.ref_code,
            experience=0,
            stones=[]
        )


class UserUpdate(BaseModel):
    username: Optional[str] = None
    full_name: Optional[str] = None
    photo_url: Optional[str] = None


class User(BaseUser):
    mnemonic: Optional[str] = None

    @property
    def is_locked(self) -> bool:
        return True


class UserBasicResponse(BaseModel):
    username: Optional[str] = None
    full_name: Optional[str] = None
    photo_url: Optional[str] = None
    experience: Optional[int] = 0


class UserResponse(BaseUser):
    pass
