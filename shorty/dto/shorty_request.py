from shorty.exception.validation_exception import ValidationException
from shorty.service.shorty_service import ShortyService
from shorty.validation.url_validator import UrlValidator

class ShortyRequest:

    def __init__(self, url, provider):
        self.url = url
        self.provider = provider

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        if url is None:
            raise ValidationException('empty_url_input', "'url' is missing")
        if not UrlValidator.is_valid(url):
            raise ValidationException('invalid_url_input',"'url' contains an invalid URL")
        self.__url = url

    @property
    def provider(self):
        return self.__provider

    @provider.setter
    def provider(self, provider):
        if provider is None:
            provider = ShortyService.get_default_provider_name()
        else:
            provider, provider_names = provider.lower(), ShortyService.get_provider_names()
            if provider not in provider_names:
                raise ValidationException('invalid_provider_name', f"'provider' expected to be one of {', '.join(provider_names)!r}")
        self.__provider = provider