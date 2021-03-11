from http import HTTPStatus

import pytest
from shorty.exception.validation_exception import ValidationException
from shorty.service.shorty_service import ShortyService

@pytest.mark.parametrize(
    'selected_provider_name',[
        None,
        'tinyurl',
        'bitly',
        'bitlyclone'
    ]
)
def test_provider_chain_depth_equals_to_number_of_available_providers(selected_provider_name):
    # GIVEN method parameters
    # WHEN
    chain = ShortyService.get_provider_chain(selected_provider_name)
    depth = 1
    while True:
        chain = chain._next_provider
        if chain is not None:
            depth = depth + 1
        else:
            break
    # THEN
    assert depth == len(ShortyService.get_provider_names())

@pytest.mark.parametrize(
    "selected_provider_name, expected_ex_code, expected_ex_message, expected_ex_status",[
        ('invalid_provider_name_value', 'invalid_provider_name', f"'provider' expected to be one of {', '.join(ShortyService.get_provider_names())!r}", HTTPStatus.UNPROCESSABLE_ENTITY)
    ]
)
def test_provider_chain_when_selected_provider_is_invalid(selected_provider_name, expected_ex_code, expected_ex_message, expected_ex_status):
    # GIVEN method parameters
    # WHEN
    with pytest.raises(ValidationException) as ex_info:
        ShortyService.get_provider_chain(selected_provider_name)
    ex = ex_info.value
    # THEN
    assert ex.code == expected_ex_code
    assert ex.message == expected_ex_message
    assert ex.status == expected_ex_status

# TODO
# def test_provider_chain_when_a_provider_fails():
#     # GIVEN