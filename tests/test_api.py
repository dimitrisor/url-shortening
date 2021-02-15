import pytest
from http import HTTPStatus

def test_api_when_request_is_valid(post):
    # GIVEN
    cls = "http://www.example.com"
    provider = "bitly"
    # WHEN
    request_data = {"cls":cls, "provider":provider}
    response = post('/shortlinks',data=request_data)

    # THEN
    response_data = response.get_json()
    assert response.status_code == HTTPStatus.OK.real
    assert response_data['cls'] == cls
    assert response_data['link'] is not None

@pytest.mark.parametrize(
    "post, cls, provider, expected_status, expected_message",[
        ("post", '://www.example.com', 'bitly', HTTPStatus.UNPROCESSABLE_ENTITY, "'cls' contains an invalid URL"),
        ("post", None, 'bitly', HTTPStatus.UNPROCESSABLE_ENTITY, "'cls' is missing"),
        ("post", "https://www.example.com", 'another provider', HTTPStatus.UNPROCESSABLE_ENTITY, "'provider' expected to be one of 'tinyurl, bitly'")
    ], indirect=["post"]
)
def test_api_when_request_is_invalid(post, cls, provider, expected_status, expected_message):
    # GIVEN method parameters
    # WHEN
    request_data = {"cls":cls, "provider":provider}
    response = post('/shortlinks',data=request_data)

    # THEN
    response_data = response.get_json()
    assert response.status_code == int(expected_status)
    assert response_data == {"message":expected_message}