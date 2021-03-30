from abc import abstractmethod
from flask import current_app
from requests import Response
from shorty.exception.provider_exception import ProviderException
from shorty.service.provider.provider import Provider

class BaseProvider(Provider):
    _next_provider: Provider = None
    # _prevous_provider: Provider = None

    def set_next(self, provider: Provider) -> Provider:
        self._next_provider = provider
        # provider._prevous_provider = self
        return provider

    @abstractmethod
    def get_shortlink(self, url: str) -> str:
        if self._next_provider:
            return self._next_provider.get_shortlink(url)

        current_app.logger.error('No shortening providers available at the moment')
        raise ProviderException('no_available_provider')

    @abstractmethod
    def post_data(self, url: str) -> Response:
        pass