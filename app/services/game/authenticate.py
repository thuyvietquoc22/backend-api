from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from loguru import logger

from app.decorator import singleton
from app.services.game.user import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@singleton
class AuthenticateService:

    def __init__(self):
        self.user_service = UserService()

    def validate_token(self, token: Annotated[str, Depends(oauth2_scheme)]):
        logger.info(f"Token: {token}")
        return self.user_service.get_user_info_by_token(token)
