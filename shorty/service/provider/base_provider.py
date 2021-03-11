from abc import abstractmethod
from flask import current_app
from shorty.exception.provider_exception import ProviderException
from shorty.service.provider.provider import Provider

class BaseProvider(Provider):
    _next_provider: Provider = None

    def set_next(self, provider: Provider) -> Provider:
        self._next_provider = provider
        return provider

    @abstractmethod
    def get_shortlink(self, url: str) -> str:
        if self._next_provider:
            return self._next_provider.get_shortlink(url)

        current_app.logger.error('No shortening providers available at the moment')
        raise ProviderException('no_available_provider')