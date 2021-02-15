from shorty.service.provider.provider import Provider
from shorty.service.provider.bitly_provider import BitlyProvider
from shorty.service.provider.tinyurl_provider import TinyUrlProvider

class ShortyService:
    default_provider_name = 'tinyurl'
    providers = {"tinyurl":TinyUrlProvider, "bitly":BitlyProvider}

    @classmethod
    def get_provider_chain(cls, selected_name: str) -> Provider:
        selected_provider = cls.providers.get(selected_name)()
        for provider_name in cls.providers.keys():
            if provider_name != selected_name:
                next_provider = cls.providers.get(provider_name)
                selected_provider.set_next(next_provider())
        return selected_provider

    @classmethod
    def get_provider_names(cls) -> list:
        return cls.providers.keys()

    @classmethod
    def get_default_provider_name(cls) -> str:
        return cls.default_provider_name