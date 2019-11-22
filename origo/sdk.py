import logging
import requests
import json

from origo.config import Config
from origo.auth.auth import Authenticate
from origo.exceptions import ApiAuthenticateError

log = logging.getLogger()


class SDK:
    def __init__(self, config=None, auth=None, env=None):
        self.config = config
        if self.config is None:
            log.info("Initializing configuration object")
            self.config = Config(env=env)
        self.auth = auth
        if self.auth is None:
            log.info("Initializing auth object")
            self.auth = Authenticate(self.config)

    def login(self):
        self.auth.login()

    def headers(self):
        headers = {}
        if self.auth.token_provider:
            headers["Authorization"] = f"Bearer {self.auth.access_token}"
        return headers

    def post(self, url, data):
        headers = self.headers()
        log.info(f"SDK:Posting resource to url: {url}")
        result = requests.post(url, data=json.dumps(data), headers=headers)
        # TODO: ensure we deal with status_code correctly here
        status_exclude = [409, 204, 201]
        if result.status_code != 200 and result.status_code not in status_exclude:
            msg = result.json()
            log.info(f"SDK:Raising error: {msg}")
            raise ApiAuthenticateError(f"Could not post data to {url}: {msg}")
        return result

    def get(self, url):
        headers = self.headers()
        log.info(f"SDK:Getting resource from url: {url}")
        result = requests.get(url, headers=headers)
        if result.status_code == 401:
            msg = result.json()
            log.info(f"Could not authenticate client, raising error: {msg}")
            raise ApiAuthenticateError(
                f"Could not authenticate client to get datasets: {msg}"
            )
        return result
