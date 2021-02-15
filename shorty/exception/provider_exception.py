from http import HTTPStatus
from shorty.exception.system_exception import SystemException
SERVICE_UNAVAILABLE_MESSAGE = "Something went wrong on our side, please try again later"
class ProviderException(SystemException):
    def __init__(self, code: str):
        super().__init__(HTTPStatus.SERVICE_UNAVAILABLE, code, self.SERVICE_UNAVAILABLE_MESSAGE)