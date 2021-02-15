from http import HTTPStatus
from shorty.exception.system_exception import SystemException

class RequestValidator:

    @staticmethod
    def validate(request):
        try:
            request_data = request.get_json()
            if request_data is None:
                raise Exception
        except Exception as ex:
            raise SystemException(HTTPStatus.BAD_REQUEST, 'invalid_body')