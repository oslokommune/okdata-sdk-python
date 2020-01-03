import logging
import requests
import json

from origo.config import Config
from origo.auth.auth import Authenticate
from origo.exceptions import ApiAuthenticateError

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
        headers = self.headers()
        log.info(f"SDK:Posting resource to url: {url}")
        result = requests.post(url, data=json.dumps(data), headers=headers, **kwargs)
        # TODO: ensure we deal with status_code correctly here
        bad_requests_exclude = [409]
        if result.status_code >= 500:
            log.info(f"SDK:Raising Internal error")
            result.raise_for_status()
        elif (
            result.status_code >= 400 and result.status_code not in bad_requests_exclude
        ):
            log.info(f"SDK:Raising Bad Request: {result.json()}")
            if result.status_code in [401, 403]:
                raise ApiAuthenticateError(f"Bad Credentials: {result.status_code}")
            result.raise_for_status()
        return result

    def get(self, url, **kwargs):
        headers = self.headers()
        log.info(f"SDK:Getting resource from url: {url}")
        result = requests.get(url, headers=headers, **kwargs)
        if result.status_code == 401:
            msg = result.json()
            log.info(f"Could not authenticate client, raising error: {msg}")
            raise ApiAuthenticateError(
                f"Could not authenticate client to get datasets: {msg}"
            )
        return result

    def delete(self, url, **kwargs):
        headers = self.headers()
        log.info(f"SDK:Deleting resource from url: {url}")
        result = requests.delete(url, headers=headers, **kwargs)
        if result.status_code == 401:
            msg = result.json()
            log.info(f"Could not authenticate client, raising error: {msg}")
            raise ApiAuthenticateError(
                f"Could not authenticate client to get datasets: {msg}"
            )
        return result
