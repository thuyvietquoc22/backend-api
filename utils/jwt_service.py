from abc import abstractmethod, ABC
from datetime import datetime, timedelta
from typing import Union, Any

import jwt
from jwt.jwk import OctetJWK
from loguru import logger

from core.config import settings
from decorator import singleton


class JWTSerializer(ABC):

    @property
    @abstractmethod
    def payload(self) -> dict[str, Any]:
        return {}


@singleton
class JWTService:

    @property
    def security_algorithm(self):
        return "HS256"

    @property
    def secret_key(self) -> OctetJWK:
        return OctetJWK(bytes(settings.SECRET_KEY, 'utf-8'))

    def generate_token(self, payload: Union[str | JWTSerializer]) -> str:
        expire = datetime.now() + timedelta(
            seconds=60 * 60 * settings.TOKEN_EXPIRED_TIME
        )

        if isinstance(payload, JWTSerializer):
            to_encode = payload.payload
        else:
            to_encode = {"sub": str(payload)}
        to_encode.update({"exp": int(expire.timestamp())})

        encoded_jwt = jwt.JWT().encode(to_encode, self.secret_key, alg=self.security_algorithm)
        return encoded_jwt

    def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.JWT().decode(token, self.secret_key, algorithms={self.security_algorithm})
            return payload
        except Exception as e:
            logger.error(f"Error when decode token: {e}")


a = JWTService().generate_token("Xin chào")
print(a)
print(JWTService().decode_token(a))
