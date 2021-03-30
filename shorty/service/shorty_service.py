from flask import current_app
from shorty.exception.validation_exception import ValidationException
from shorty.service.provider.bitly_clone_provider import BitlyCloneProvider
from shorty.service.provider.provider import Provider
from shorty.service.provider.bitly_provider import BitlyProvider
from shorty.service.provider.tinyurl_provider import TinyUrlProvider

class ShortyService:
    provider_map = { "tinyurl":TinyUrlProvider, "bitly":BitlyProvider, "bitlyclone":BitlyCloneProvider}

    def get_provider_chain(self, selected_provider_name=None) -> Provider:
        if selected_provider_name is None:
            selected_provider_name = self.get_default_provider_name()

        try:
            selected_provider_cls = self.provider_map[selected_provider_name]
        except:
            current_app.logger.error('Invalid requested provider name')
            raise ValidationException('invalid_provider_name', f"'provider' expected to be one of {', '.join(self.provider_map.keys())!r}")

        selected_provider = selected_provider_cls()
        provider_chain = selected_provider

        for p_name, p_cls in self.provider_map.items():
            if p_name != selected_provider_name:
                selected_provider = selected_provider.set_next(p_cls())
        return provider_chain

    @classmethod
    def get_provider_names(cls) -> list:
        return list(cls.provider_map.keys())

    @classmethod
    def get_default_provider_name(cls) -> str:
        return cls.get_provider_names()[0]