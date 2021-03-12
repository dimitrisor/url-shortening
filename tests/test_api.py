import pytest
from http import HTTPStatus
from shorty.service.shorty_service import ShortyService

def test_api_when_request_is_valid(post):
    # GIVEN
    url = "http://www.example.com"
    provider = "bitly"
    endpoint = '/shortlinks'
    # WHEN
    request_data = {"url": url, "provider": provider}
    response = post(endpoint, data=request_data)

    # THEN
    response_data = response.get_json()
    assert response.status_code == HTTPStatus.OK.real
    assert response_data['url'] == url
    assert response_data['link'] is not None

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

def test_api_when_request_url_is_invalid_not_found(post):
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
