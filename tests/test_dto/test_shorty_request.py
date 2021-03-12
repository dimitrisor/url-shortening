import pytest
from http import HTTPStatus
from shorty.dto.shorty_request import ShortyRequest
from shorty.exception.validation_exception import ValidationException
from shorty.service.shorty_service import ShortyService

@pytest.mark.parametrize(
    "url, provider",[
        ('https://www.example.com', 'bitly'),
        ('http://www.example.com', 'tinyurl'),
        ('https://example.com', None),
    ]
)
def test_shorty_request_for_valid_input(url, provider):
    # GIVEN method parameters
    # WHEN
    shorty_request = ShortyRequest(url, provider)
    # THEN
    assert shorty_request.url == url
    if provider is None:
        assert shorty_request.provider == ShortyService.get_default_provider_name()
    else:
        assert shorty_request.provider == provider

@pytest.mark.parametrize(
    "url, provider, expected_ex_code, expected_ex_message, expected_ex_status",[
        ('://www.example.com', 'bitly', 'invalid_url_input', "'url' contains an invalid URL", HTTPStatus.UNPROCESSABLE_ENTITY),
        (None, 'bitly', 'empty_url_input', "'url' is missing", HTTPStatus.UNPROCESSABLE_ENTITY),
        ("https://www.example.com", 'not_available_provider', 'invalid_provider_name', f"'provider' expected to be one of {', '.join(ShortyService.get_provider_names())!r}", HTTPStatus.UNPROCESSABLE_ENTITY)
    ]
)
def test_shorty_request_for_invalid_input(url, provider, expected_ex_code, expected_ex_message, expected_ex_status):
    # GIVEN method parameters
    # WHEN
    with pytest.raises(ValidationException) as ex_info:
        ShortyRequest(url, provider)
    ex = ex_info.value
    # THEN
    assert ex.code == expected_ex_code
    assert ex.message == expected_ex_message
    assert ex.status == expected_ex_status