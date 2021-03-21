import json
from flask import current_app
import requests
from shorty.service.provider.base_provider import BaseProvider

NAME = "bitlyclone"
class BitlyCloneProvider(BaseProvider):

    def __init__(self) -> None:
        super().__init__()
        self.group_id = current_app.config['BITLY_GROUP_ID']
        self.auth_token = current_app.config['BITLY_AUTH_TOKEN']

    def get_shortlink(self, url: str) -> str:
        base_url = 'https://api-ssl.bitly.com/v4/'
        endpoint = base_url + 'shorten'
        payload = {"group_guid" : self.group_id, "domain" : "bit.ly", "long_url" : url}
        headers = {"Authorization" : "Bearer " + self.auth_token, "Content-Type" : "application/json"}

        try:
            response = requests.post(url = endpoint, data = json.dumps(payload), headers = headers, timeout = 5)
            response.raise_for_status()
            return response.json()['link'] + 'copy'
        except requests.exceptions.RequestException:
            msg = "Shortening provider '{}' is not available".format(NAME)
            current_app.logger.warn(msg)
            return super().get_shortlink(url)