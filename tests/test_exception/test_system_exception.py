from http import HTTPStatus

from shorty.exception.system_exception import SystemException

def test_system_exception_properties_when_message_is_passed():
    # GIVEN
    status = HTTPStatus.SERVICE_UNAVAILABLE
    code = 'no_available_provider'
    message = 'No shortening providers available at the moment'
    # WHEN
    exception = SystemException(status, code, message)
    # THEN
    assert exception.get_status() == status
    assert exception.get_code() == code
    assert exception.get_message() == message

def test_system_exception_properties_when_message_is_not_passed():
    # GIVEN
    status = HTTPStatus.SERVICE_UNAVAILABLE
    code = 'no_available_provider'
    default_message = "Please provide a valid JSON body with 'url' and 'provider' parameters"
    # WHEN
    exception = SystemException(status, code)
    # THEN
    assert exception.get_status() == status
    assert exception.get_code() == code
    assert exception.get_message() == default_message