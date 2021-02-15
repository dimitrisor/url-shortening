import pytest
from shorty.validation.url_validator import UrlValidator

@pytest.mark.parametrize("url", ['', None])
def test_url_validator_WHEN_missing_or_empty_value(url):
    # GIVEN 'url' method parameter
    # WHEN
    is_valid = UrlValidator.is_valid(url)
    # THEN
    assert not is_valid

@pytest.mark.parametrize("url", ['invalid://www.example.com', '://www.example.com', 'http:/www.example.com', 'www.example.com'])
def test_url_validator_WHEN_invalid_protocol(url):
    # GIVEN 'url' method parameter
    # WHEN
    is_valid = UrlValidator.is_valid(url)
    # THEN
    assert not is_valid

def test_url_validator_WHEN_missing_domain():
    # GIVEN
    url = "https://.com"
    # WHEN
    is_valid = UrlValidator.is_valid(url)
    # THEN
    assert not is_valid

def test_url_validator_WHEN_missing_domain_extension():
    # GIVEN
    url = "https://example."
    # WHEN
    is_valid = UrlValidator.is_valid(url)
    # THEN
    assert not is_valid

def test_url_validator_WHEN_invalid_format():
    # GIVEN
    url = "https://www. example.com"
    # WHEN
    is_valid = UrlValidator.is_valid(url)
    # THEN
    assert not is_valid

def test_url_validator_WHEN_email_is_number():
    # GIVEN
    url = 123
    # WHEN
    is_valid = UrlValidator.is_valid(url)
    # THEN
    assert not is_valid

@pytest.mark.parametrize(
    'url',[
        'http://example.com',
        'https://example.com',
        'http://www.example.com',
        'https://www.example.com',
        'https://example.com/example',
        'https://example.com/search?url_parma1=parma1&url_parma2=param2'
    ]
)
def test_url_validator_WHEN_email_is_valid(url):
    # GIVEN 'url' method parameter
    # WHEN
    is_valid = UrlValidator.is_valid(url)
    # THEN
    assert is_valid