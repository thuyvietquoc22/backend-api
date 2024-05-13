from typing import Optional

from pydantic import BaseModel

from entity.core import BaseMongoModel


class BaseUser(BaseMongoModel):
    tele_id: int
    username: Optional[str] = None
    full_name: Optional[str] = None
    photo_url: Optional[str] = None
    ref_code: Optional[int] = None
    level: Optional[int] = 0
    experience: Optional[int] = 0


class UserRegister(BaseModel):
    tele_id: int
    username: Optional[str] = None
    full_name: Optional[str] = None
    photo_url: Optional[str] = None
    ref_code: Optional[int] = None


class UserCreate(BaseUser):
    pass

    @classmethod
    def from_register(cls, register: UserRegister):
        return cls(
            tele_id=register.tele_id,
            user_name=register.username,
            full_name=register.full_name,
            photo_url=register.photo_url,
            ref_code=register.ref_code,
            level=0,
            experience=0
        )


class UserUpdate(BaseModel):
    username: Optional[str] = None
    full_name: Optional[str] = None
    photo_url: Optional[str] = None


class UserResponse(BaseUser):
    pass
