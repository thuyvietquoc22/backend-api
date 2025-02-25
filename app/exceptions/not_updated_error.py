from http import HTTPStatus

from app.exceptions.base_exception import BaseExceptionMixin


class NotUpdatedError(BaseExceptionMixin):
    message = "Not updated"
    status = HTTPStatus.INTERNAL_SERVER_ERROR
