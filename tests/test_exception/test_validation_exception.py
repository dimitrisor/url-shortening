from http import HTTPStatus
from shorty.exception.validation_exception import ValidationException

def test_validation_exception_get_status_code_message():
    # GIVEN
    code = 'empty_url'
    message = "'url' is missing"
    # WHEN
    exception = ValidationException(code, message)
    # THEN
    assert exception.get_status() == HTTPStatus.UNPROCESSABLE_ENTITY
    assert exception.get_code() == code
    assert exception.get_message() == message