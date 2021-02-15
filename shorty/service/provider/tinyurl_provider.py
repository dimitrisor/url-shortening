from flask import current_app
import requests
from shorty.service.provider.base_provider import BaseProvider

NAME = "tinyurl"
class TinyUrlProvider(BaseProvider):

    def get_shortlink(self, url : str) -> str:
        base_url = 'https://tinyurl.com/'
        endpoint = base_url + 'api-create.php'
        payload = {"url" : url}
        try:
            response = requests.post(url = endpoint, data = payload, timeout = 5)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException:
            msg = "Shortening provider '{}' is not available".format(NAME)
            current_app.logger.warn(msg)
            return super().get_shortlink(url)