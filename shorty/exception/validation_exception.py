from http import HTTPStatus
from shorty.exception.system_exception import SystemException

class ValidationException(SystemException):
    def __init__(self, code: str, message):
        super().__init__(HTTPStatus.UNPROCESSABLE_ENTITY, code, message)