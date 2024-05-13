from http import HTTPStatus

from exceptions.base_exception import BaseExceptionMixin


class AuthenticateException(BaseExceptionMixin):

    def __init__(self, message: str = "Unauthorized"):
        self.message = message
        self.status = HTTPStatus.UNAUTHORIZED
