from http import HTTPStatus
import pytest
from unittest.mock import Mock, MagicMock
from requests import RequestException
from shorty.exception.provider_exception import ProviderException
from shorty.exception.validation_exception import ValidationException
from shorty.service.shorty_service import ShortyService

@pytest.fixture
def provider_names():
    return list(ShortyService.provider_map.keys())

@pytest.fixture
def mock_fail_response():
    mock_resp = Mock()
    mock_resp.status_code = 400
    mock_resp.raise_for_status = Mock(side_effect = RequestException)
    return mock_resp

def test_get_provider_names(provider_names):
    assert ShortyService.get_provider_names() == provider_names

def test_get_default_provider_name(provider_names):
    assert ShortyService.get_default_provider_name() == provider_names[0]

def test_provider_chain_when_selected_provider_is_invalid():
    # GIVEN
    selected_provider_name = 'invalid_provider_name_value'
    expected_ex_code = 'invalid_provider_name'
    expected_ex_message = f"'provider' expected to be one of {', '.join(ShortyService.get_provider_names())!r}"
    expected_ex_status = HTTPStatus.UNPROCESSABLE_ENTITY
    try:
        ShortyService().get_provider_chain(selected_provider_name)
    except ValidationException as ex:
        # THEN
        assert ex.code == expected_ex_code
        assert ex.message == expected_ex_message
        assert ex.status == expected_ex_status

@pytest.mark.parametrize(
    'selected_provider_name',[
        None, # Returns the default one, in our case the TinyUrlProvider
        'tinyurl',
        'bitly',
        'bitlyclone'
    ]
)
def test_first_provider_in_chain_is_the_one_requested(provider_names, selected_provider_name):
    # GIVEN selected_provider_name
    service = ShortyService()
    defaut_provider_name = provider_names[0]

    if selected_provider_name is not None:
        expected_provider_type = service.provider_map[selected_provider_name]
    else:
        expected_provider_type = service.provider_map[defaut_provider_name]
        service.get_default_provider_name = MagicMock(return_value=defaut_provider_name)
    # WHEN
    actual_provider_type = type(service.get_provider_chain(selected_provider_name))
    # THEN
    assert expected_provider_type == actual_provider_type
    if selected_provider_name is None:
        service.get_default_provider_name.assert_called_once()

def test_provider_chain_depth_equals_to_number_of_available_providers():
    # GIVEN method parameters
    # WHEN
    chain = ShortyService().get_provider_chain()
    depth = 1
    while True:
        chain = chain._next_provider
        if chain is not None:
            depth += 1
        else:
            break
    # THEN
    assert depth == len(ShortyService.get_provider_names())


def test_provider_chain_when_first_provider_works():
    # GIVEN
    provider_it = iter(ShortyService.provider_map.values())
    tinyurl_provider, bitly_provider, bitly_clone_provider = next(provider_it), next(provider_it), next(provider_it)
    valid_url = 'https://example.com'

    # Mock BitlyProvider's Response, and assign it to its post_data method
    mock_tinyurl_post_resp = Mock()
    mock_tinyurl_post_resp.status_code = 200
    tinyurl_provider.post_data = Mock(return_value = mock_tinyurl_post_resp)

    bitly_provider.post_data = Mock()
    bitly_clone_provider.post_data = Mock()

    # WHEN
    ShortyService().get_provider_chain().get_shortlink(valid_url)

    # THEN
    tinyurl_provider.post_data.assert_called_once()
    bitly_provider.post_data.assert_not_called()
    bitly_clone_provider.post_data.assert_not_called()


def test_provider_chain_when_first_provider_fails(mock_fail_response):
    # GIVEN
    provider_it = iter(ShortyService.provider_map.values())
    tinyurl_provider, bitly_provider, bitly_clone_provider = next(provider_it), next(provider_it), next(provider_it)
    valid_url = 'https://example.com'

    # Mock TinyUrlProvider's Response, and assign it to its post_data method
    tinyurl_provider.post_data = Mock(return_value = mock_fail_response)

    # Mock BitlyProvider's Response, and assign it to its post_data method
    mock_bitly_post_resp = Mock()
    mock_bitly_post_resp.status_code = 200
    mock_bitly_post_resp.json = Mock(return_value = {'link': 'https://bit.ly/example'})
    bitly_provider.post_data = Mock(return_value = mock_bitly_post_resp)

    bitly_clone_provider.post_data = Mock()

    # WHEN
    ShortyService().get_provider_chain().get_shortlink(valid_url)

    # THEN
    tinyurl_provider.post_data.assert_called_once()
    bitly_provider.post_data.assert_called_once()
    bitly_clone_provider.post_data.assert_not_called()


def test_provider_chain_when_first_and_second_provider_fails(mock_fail_response):
    # GIVEN
    provider_it = iter(ShortyService.provider_map.values())
    tinyurl_provider, bitly_provider, bitly_clone_provider = next(provider_it), next(provider_it), next(provider_it)
    valid_url = 'https://example.com'

    # Mock TinyUrlProvider's Response, and assign it to its post_data method
    tinyurl_provider.post_data = Mock(return_value = mock_fail_response)

    # Mock BitlyProvider's Response, and assign it to its post_data method
    bitly_provider.post_data = Mock(return_value = mock_fail_response)

    # Mock BitlyCloneProvider's Response, and assign it to its post_data method
    mock_bitly_clone_post_resp = Mock()
    mock_bitly_clone_post_resp.status_code = 200
    mock_bitly_clone_post_resp.json = Mock(return_value = {'link': 'https://bit.ly/example'})
    bitly_clone_provider.post_data = Mock(return_value = mock_bitly_clone_post_resp)

    # WHEN
    ShortyService().get_provider_chain().get_shortlink(valid_url)

    # THEN
    tinyurl_provider.post_data.assert_called_once()
    bitly_provider.post_data.assert_called_once()
    bitly_clone_provider.post_data.assert_called_once()


def test_provider_chain_when_all_providers_fail(mock_fail_response):
    # GIVEN
    provider_it = iter(ShortyService.provider_map.values())
    tinyurl_provider, bitly_provider, bitly_clone_provider = next(provider_it), next(provider_it), next(provider_it)
    valid_url = 'https://example.com'
    expected_ex_code = "no_available_provider"
    expected_ex_message = "Something went wrong on our side, please try again later"
    expected_ex_status = HTTPStatus.SERVICE_UNAVAILABLE

    # Mock TinyUrlProvider's Response, and assign it to its post_data method
    tinyurl_provider.post_data = Mock(return_value = mock_fail_response)

    # Mock BitlyProvider's Response, and assign it to its post_data method
    bitly_provider.post_data = Mock(return_value = mock_fail_response)

    # Mock BitlyCloneProvider's Response, and assign it to its post_data method
    bitly_clone_provider.post_data = Mock(return_value = mock_fail_response)
    # WHEN
    with pytest.raises(ProviderException) as ex_info:
        ShortyService().get_provider_chain().get_shortlink(valid_url)
    ex = ex_info.value

    assert ex.code == expected_ex_code
    assert ex.message == expected_ex_message
    assert ex.status == expected_ex_status

    # THEN
    tinyurl_provider.post_data.assert_called_once()
    bitly_provider.post_data.assert_called_once()
    bitly_clone_provider.post_data.assert_called_once()