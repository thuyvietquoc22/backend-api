from abc import abstractmethod, ABC
from datetime import datetime, timedelta
from typing import Union, Any, TypeVar, Generic

import jwt
from jwt.jwk import OctetJWK

from app.core.config import settings
from app.decorator import singleton


class JWTSerializer(ABC):

    @property
    @abstractmethod
    def to_encode(self) -> dict[str, Any]:
        return {}

    @staticmethod
    def from_payload(payload: dict) -> Any:
        return payload


@singleton
class JWTService:

    @property
    def security_algorithm(self):
        return "HS256"

    @property
    def secret_key(self) -> OctetJWK:
        return OctetJWK(bytes(settings.SECRET_KEY, 'utf-8'))

    def generate_token(self, payload: Union[Any | JWTSerializer], time_expired: datetime = None) -> str:
        expire = time_expired or datetime.now() + timedelta(
            seconds=60 * 60 * settings.TOKEN_EXPIRED_TIME
        )

        if isinstance(payload, JWTSerializer):
            to_encode = payload.to_encode
        else:
            to_encode = {}
            to_encode.update(payload)
        to_encode.update({"exp": int(expire.timestamp())})

        encoded_jwt = jwt.JWT().encode(to_encode, self.secret_key, alg=self.security_algorithm)
        return encoded_jwt

    def decode_token(self, token: str) -> dict:
        payload = jwt.JWT().decode(token, self.secret_key, algorithms={self.security_algorithm})
        return payload or {}
