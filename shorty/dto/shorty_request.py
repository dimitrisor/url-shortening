from shorty.exception.validation_exception import ValidationException
from shorty.service.shorty_service import ShortyService
from shorty.validation.url_validator import UrlValidator

class ShortyRequest:

    def __init__(self, cls, provider):
        self.cls = cls
        self.provider = provider

    @property
    def cls(self):
        return self.__cls

    @cls.setter
    def cls(self, cls):
        if cls is None:
            raise ValidationException('empty_cls_input', "'cls' is missing")
        if not UrlValidator.is_valid(cls):
            raise ValidationException('invalid_cls_input',"'cls' contains an invalid URL")
        self.__cls = cls

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