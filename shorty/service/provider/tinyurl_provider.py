from flask import current_app
import requests
from requests import Response
from shorty.service.provider.base_provider import BaseProvider

NAME = "tinyurl"
class TinyUrlProvider(BaseProvider):

    def get_shortlink(self, url : str) -> str:
        try:
            response = self.post_data(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException:
            msg = "Shortening provider '{}' is n3ot available".format(NAME)
            current_app.logger.warn(msg)
            return super().get_shortlink(url)

    def post_data(self, url: str) -> Response:
        base_url = 'https://tinyurl.com/'
        endpoint = base_url + 'api-create.php'
        payload = {"url" : url}
        return requests.post(url = endpoint, data = payload, timeout = 5)