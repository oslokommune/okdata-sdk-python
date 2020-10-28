import logging
import requests
import json

from origo.config import Config
from origo.auth.auth import Authenticate

log = logging.getLogger()


class SDK(object):
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

    def post(self, url, data, **kwargs):
        log.info(f"SDK:Posting resource to url: {url}")
        result = requests.post(
            url, data=json.dumps(data), headers=self.headers(), **kwargs
        )
        result.raise_for_status()
        return result

    def put(self, url, data, **kwargs):
        log.info(f"SDK:Putting resource to url: {url}")
        result = requests.put(
            url, data=json.dumps(data), headers=self.headers(), **kwargs
        )
        result.raise_for_status()
        return result

    def get(self, url, **kwargs):
        log.info(f"SDK:Getting resource from url: {url}")
        result = requests.get(url, headers=self.headers(), **kwargs)
        result.raise_for_status()
        return result

    def delete(self, url, **kwargs):
        log.info(f"SDK:Deleting resource from url: {url}")
        result = requests.delete(url, headers=self.headers(), **kwargs)
        result.raise_for_status()
        return result
