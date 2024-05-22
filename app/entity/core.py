from abc import ABC, abstractmethod
from typing import Annotated, Optional

from pydantic import BeforeValidator, Field, ConfigDict, BaseModel

PyObjectId = Annotated[str, BeforeValidator(str)]


class BaseMongoModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class UserDetails(ABC):
    @abstractmethod
    def is_locked(self) -> bool:
        pass

    @property
    @abstractmethod
    def password(self) -> str:
        pass

    @property
    @abstractmethod
    def username(self) -> str:
        pass


class StringBody(BaseModel):
    content: str


class IntBody(BaseModel):
    value: int
