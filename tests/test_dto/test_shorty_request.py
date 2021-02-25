import pytest
from http import HTTPStatus
from shorty.dto.shorty_request import ShortyRequest
from shorty.exception.validation_exception import ValidationException
from shorty.service.shorty_service import ShortyService

@pytest.mark.parametrize(
    "cls, provider",[
        ('https://www.example.com', 'bitly'),
        ('https://www.example.com', 'tinyurl'),
        ('https://www.example.com', None),
    ]
)
def test_shorty_request_for_valid_input(cls, provider):
    # GIVEN method parameters
    # WHEN
    shorty_request = ShortyRequest(cls, provider)
    # THEN
    assert shorty_request.cls == cls
    if provider is None:
        assert shorty_request.provider == ShortyService.get_default_provider_name()
    else:
        assert shorty_request.provider == provider

@pytest.mark.parametrize(
    "cls, provider, expected_ex_code, expected_ex_message, expected_ex_status",[
        ('://www.example.com', 'bitly', 'invalid_cls_input', "'cls' contains an invalid URL", HTTPStatus.UNPROCESSABLE_ENTITY),
        (None, 'bitly', 'empty_cls_input', "'cls' is missing", HTTPStatus.UNPROCESSABLE_ENTITY),
        ("https://www.example.com", 'not_available_provider', 'invalid_provider_name', f"'provider' expected to be one of {', '.join(ShortyService.get_provider_names())!r}", HTTPStatus.UNPROCESSABLE_ENTITY)
    ]
)
def test_shorty_request_for_invalid_cls_input(cls, provider, expected_ex_code, expected_ex_message, expected_ex_status):
    # GIVEN method parameters
    # WHEN
    with pytest.raises(ValidationException) as ex_info:
        ShortyRequest(cls, provider)
    ex = ex_info.value
    print('')
    # THEN
    assert ex.code == expected_ex_code
    assert ex.message == expected_ex_message
    assert ex.status == expected_ex_status