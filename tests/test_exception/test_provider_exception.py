from http import HTTPStatus
from shorty.exception.provider_exception import ProviderException

def test_validation_exception_get_status_code_message():
    # GIVEN
    code = 'no_available_provider'
    message = 'Something went wrong on our side, please try again later'
    # WHEN
    exception = ProviderException(code)
    # THEN
    assert exception.get_status() == HTTPStatus.SERVICE_UNAVAILABLE
    assert exception.get_code() == code
    assert exception.get_message() == message