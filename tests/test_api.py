from unittest.mock import Mock
import pytest
from http import HTTPStatus
from shorty.service.provider.bitly_provider import BitlyProvider
from shorty.service.shorty_service import ShortyService

def mock_bitly_provider(expected_link):
    # Mock post_data, avoid calling the real requests.post
    mock_bitly_post_resp = Mock()
    mock_bitly_post_resp.status_code = 200
    mock_bitly_post_resp.json = Mock(return_value = {'link': expected_link})
    BitlyProvider.post_data = Mock(return_value = mock_bitly_post_resp)

def test_api_when_request_is_valid(post):
    # GIVEN
    url = "http://www.example.com"
    provider = "bitly"
    endpoint = '/shortlinks'

    expected_link = 'https://bit.ly/example'
    mock_bitly_provider(expected_link)
    # WHEN
    response = post(endpoint, data={"url": url, "provider": provider})

    # THEN
    response_data = response.get_json()
    assert response.status_code == HTTPStatus.OK.real
    assert response_data['url'] == url
    assert response_data['link'] == expected_link

@pytest.mark.parametrize(
    "post, url, provider, expected_status, expected_message",[
        ("post", '://www.example.com', 'bitly', HTTPStatus.UNPROCESSABLE_ENTITY, "'url' contains an invalid URL"),
        ("post", None, 'bitly', HTTPStatus.UNPROCESSABLE_ENTITY, "'url' is missing"),
        ("post", "https://www.example.com", 'another provider', HTTPStatus.UNPROCESSABLE_ENTITY,
         f"'provider' expected to be one of {', '.join(ShortyService.get_provider_names())!r}")
    ], indirect=["post"]
)
def test_api_when_request_payload_is_invalid(post, url, provider, expected_status, expected_message):
    # GIVEN method parameters
    endpoint = '/shortlinks'
    # WHEN
    request_data = {"url": url, "provider": provider}
    response = post(endpoint, data=request_data)

    # THEN
    response_data = response.get_json()
    assert response.status_code == int(expected_status)
    assert response_data == {"message":expected_message}

def test_api_when_request_url_is_not_found(post):
    # GIVEN
    url = "http://www.example.com"
    provider = "bitly"
    invalid_endpoint = '/non_existent'
    # WHEN
    request_data = {"url": url, "provider": provider}
    response = post(invalid_endpoint, data=request_data)

    # THEN
    response_data = response.get_json()
    assert response.status_code == 404
    assert response_data == {"message": "The requested URL was not found on the server"}
