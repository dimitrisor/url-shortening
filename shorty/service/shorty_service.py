from shorty.service.provider.bitly_clone_provider import BitlyCloneProvider
from shorty.service.provider.provider import Provider
from shorty.service.provider.bitly_provider import BitlyProvider
from shorty.service.provider.tinyurl_provider import TinyUrlProvider

class ShortyService:
    provider_map = { "tinyurl":TinyUrlProvider, "bitly":BitlyProvider, "bitlyclone":BitlyCloneProvider}

    @classmethod
    def get_provider_chain(cls, selected_name: str) -> Provider:
        provider = cls.providers.get(selected_name)()
        provider_chain = provider
        for provider_name in cls.providers.keys():
            if provider_name != selected_name:
                next_provider_cls = cls.providers.get(provider_name)
                provider = provider.set_next(next_provider_cls())
        return provider_chain

    @classmethod
    def get_provider_names(cls) -> list:
        return cls.provider_map.keys()

    @classmethod
    def get_default_provider_name(cls) -> str:
        return list(cls.provider_map.keys())[0]