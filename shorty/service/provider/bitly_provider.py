import json
from flask import current_app
import requests
from shorty.service.provider.base_provider import BaseProvider

NAME = "bitly"
GROUP_ID = "Bl2b0UoNj6L"
AUTH_TOKEN = "63f57a37995caf0310c95801e1901af91433541b"
class BitlyProvider(BaseProvider):

    def get_shortlink(self, url: str) -> str:
        base_url = 'https://api-ssl.bitly.com/v4/'
        endpoint = base_url + 'shorten'
        payload = {"group_guid" : GROUP_ID, "domain" : "bit.ly", "long_url" : url}
        headers = {"Authorization" : "Bearer " + AUTH_TOKEN, "Content-Type" : "application/json"}

        try:
            response = requests.post(url = endpoint, data = json.dumps(payload), headers = headers, timeout = 5)
            response.raise_for_status()
            return response.json()['link']
        except requests.exceptions.RequestException:
            msg = "Shortening provider '{}' is not available".format(NAME)
            current_app.logger.warn(msg)
            return super().get_shortlink(url)