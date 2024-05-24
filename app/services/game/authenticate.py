from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from loguru import logger

from app.decorator import singleton
from app.exceptions.auth.authenticate_exception import AuthenticateException
from app.exceptions.parse_none_exception import ParseNoneException
from app.services.game.user import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login-for-docs")


@singleton
class AuthenticateService:

    def __init__(self):
        self.user_service = UserService()

    def validate_token(self, token: Annotated[str, Depends(oauth2_scheme)]):
        try:
            logged_user = self.user_service.get_user_info_by_token(token)
            return logged_user
        except ParseNoneException as e:
            logger.error(e)
            return None

    def get_logged_user(self, token: Annotated[str, Depends(oauth2_scheme)]):
        user = self.validate_token(token)

        # TODO Check user is banned or not
        if user is None:
            raise AuthenticateException("Please login to continue.")

        return user
